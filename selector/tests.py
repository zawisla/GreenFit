from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse

from catalog.models import Plant, PlantCategory

from .analytics import build_statistics
from .forms import RoomConditionForm
from .matching import WEIGHTS, match_plant, rank_plants
from .models import MatchResult, RoomCondition
from .weather import WeatherError, fetch_current_weather, humidity_to_level


# --- builders -------------------------------------------------------------

def build_plant(**overrides):
    """An unsaved Plant for database-free matching tests."""
    data = dict(
        name="Растение",
        category=PlantCategory(name="Категория", slug="c"),
        light_needs="bright",
        humidity_needs="low",
        temp_min=15,
        temp_max=30,
        toxicity=False,
        care_difficulty="easy",
        water_frequency="rare",
        max_height=30,
    )
    data.update(overrides)
    return Plant(**data)


def build_room(**overrides):
    """An unsaved RoomCondition for database-free matching tests."""
    data = dict(
        light_level="bright",
        humidity="low",
        temperature=22,
        room_size="small",
        has_pets=False,
        care_time="minimal",
    )
    data.update(overrides)
    return RoomCondition(**data)


def default_category():
    category, _ = PlantCategory.objects.get_or_create(
        slug="test", defaults={"name": "Тест"}
    )
    return category


def make_plant(**overrides):
    overrides.setdefault("category", default_category())
    data = dict(
        name="Растение",
        light_needs="bright",
        humidity_needs="low",
        temp_min=15,
        temp_max=30,
        toxicity=False,
        care_difficulty="easy",
        water_frequency="rare",
        max_height=30,
    )
    data.update(overrides)
    return Plant.objects.create(**data)


# --- matching engine ------------------------------------------------------

class MatchingEngineTests(TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(WEIGHTS.values()), 100)

    def test_perfect_match_scores_100(self):
        match = match_plant(build_room(), build_plant())
        self.assertEqual(match.score, 100.0)
        self.assertEqual(match.status, "good")

    def test_six_criteria_returned(self):
        match = match_plant(build_room(), build_plant())
        self.assertEqual(len(match.criteria), 6)
        self.assertEqual(len(match.reasons_text.splitlines()), 6)

    def test_toxic_plant_with_pets_loses_safety_points(self):
        room = build_room(has_pets=True)
        toxic = match_plant(room, build_plant(toxicity=True))
        safe = match_plant(room, build_plant(toxicity=False))
        pets = next(c for c in toxic.criteria if c.key == "pets")
        self.assertEqual(pets.fraction, 0.0)
        self.assertEqual(safe.score - toxic.score, WEIGHTS["pets"])

    def test_temperature_outside_range_reduces_score(self):
        room = build_room(temperature=5)  # below the 15..30 range
        match = match_plant(room, build_plant())
        temperature = next(c for c in match.criteria if c.key == "temperature")
        self.assertLess(temperature.fraction, 1.0)

    def test_rank_plants_sorts_descending(self):
        room = build_room()
        good = build_plant(name="Хорошее")
        bad = build_plant(name="Плохое", light_needs="low", humidity_needs="high",
                          care_difficulty="hard", water_frequency="frequent",
                          max_height=250, temp_min=28, temp_max=35)
        ranked = rank_plants(room, [bad, good])
        self.assertEqual(ranked[0].plant.name, "Хорошее")
        self.assertGreaterEqual(ranked[0].score, ranked[1].score)


# --- form validation ------------------------------------------------------

class RoomConditionFormTests(TestCase):
    valid_data = {
        "light_level": "bright",
        "humidity": "low",
        "temperature": 22,
        "room_size": "small",
        "has_pets": True,
        "care_time": "minimal",
    }

    def test_valid_form(self):
        self.assertTrue(RoomConditionForm(data=self.valid_data).is_valid())

    def test_temperature_out_of_range_is_invalid(self):
        data = {**self.valid_data, "temperature": 99}
        form = RoomConditionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("temperature", form.errors)


# --- weather client (mocked network) --------------------------------------

def _response(payload):
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = payload
    return mock


class WeatherClientTests(TestCase):
    def test_humidity_to_level_boundaries(self):
        self.assertEqual(humidity_to_level(20), "low")
        self.assertEqual(humidity_to_level(55), "medium")
        self.assertEqual(humidity_to_level(80), "high")

    @patch("selector.weather.requests.get")
    def test_fetch_current_weather_success(self, mock_get):
        mock_get.side_effect = [
            _response({"results": [
                {"latitude": 55.75, "longitude": 37.61, "name": "Moscow", "country": "Russia"}
            ]}),
            _response({"current": {"temperature_2m": 19.4, "relative_humidity_2m": 73}}),
        ]
        snapshot = fetch_current_weather("Moscow")
        self.assertEqual(snapshot.temperature, 19)
        self.assertEqual(snapshot.humidity_percent, 73)
        self.assertEqual(snapshot.humidity_level, "high")
        self.assertIn("Moscow", snapshot.place)

    @patch("selector.weather.requests.get")
    def test_fetch_current_weather_city_not_found(self, mock_get):
        mock_get.side_effect = [_response({"results": []})]
        with self.assertRaises(WeatherError):
            fetch_current_weather("Неизвестный город")


# --- views and full selection flow ----------------------------------------

class SelectionFlowTests(TestCase):
    def setUp(self):
        self.p1 = make_plant(name="Эхеверия", max_height=15)
        self.p2 = make_plant(name="Монстера", max_height=250, toxicity=True)

    def test_post_creates_room_results_and_redirects(self):
        response = self.client.post(reverse("selector:select"), {
            "light_level": "bright",
            "humidity": "low",
            "temperature": 22,
            "room_size": "small",
            "has_pets": False,
            "care_time": "minimal",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RoomCondition.objects.count(), 1)
        self.assertEqual(MatchResult.objects.count(), 2)

    def test_result_page_renders_ranked_list(self):
        room = RoomCondition.objects.create(
            light_level="bright", humidity="low", temperature=22,
            room_size="small", has_pets=False, care_time="minimal",
        )
        response = self.client.get(reverse("selector:result", args=[room.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Эхеверия")
        self.assertContains(response, "совместимость")

    def test_result_pet_safe_filter_hides_toxic(self):
        room = RoomCondition.objects.create(
            light_level="bright", humidity="low", temperature=22,
            room_size="small", has_pets=True, care_time="minimal",
        )
        response = self.client.get(
            reverse("selector:result", args=[room.pk]), {"pet_safe": "on"}
        )
        self.assertContains(response, "Эхеверия")
        self.assertNotContains(response, "Монстера")

    def test_history_requires_login(self):
        response = self.client.get(reverse("selector:history"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)


# --- statistics aggregation ----------------------------------------------

class AnalyticsTests(TestCase):
    def test_build_statistics_empty(self):
        stats = build_statistics()
        self.assertFalse(stats["has_data"])

    def test_build_statistics_with_data(self):
        plant = make_plant(name="Алоэ", care_difficulty="easy")
        room = RoomCondition.objects.create(
            light_level="bright", humidity="low", temperature=22,
            room_size="small", has_pets=False, care_time="minimal",
        )
        MatchResult.objects.create(room=room, plant=plant, match_score=90.0, reasons="x")
        MatchResult.objects.create(room=room, plant=plant, match_score=80.0, reasons="y")
        stats = build_statistics()
        self.assertTrue(stats["has_data"])
        self.assertEqual(stats["average_score"], 85.0)
        self.assertEqual(stats["top_plants"][0]["name"], "Алоэ")
