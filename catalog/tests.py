from pathlib import Path

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from catalog.models import Plant, PlantCategory
from catalog.plant_data import CATEGORIES, PLANTS

SEED_IMAGES_DIR = Path(__file__).resolve().parent / "seed_images"


class PlantCatalogueDataTests(SimpleTestCase):
    """Guard rails for the hand-written catalogue in ``catalog.plant_data``."""

    def test_catalogue_has_at_least_100_plants(self):
        self.assertGreaterEqual(len(PLANTS), 100)

    def test_plant_names_are_unique(self):
        names = [plant["name"] for plant in PLANTS]
        duplicates = {name for name in names if names.count(name) > 1}
        self.assertEqual(duplicates, set(), f"Дубликаты названий: {duplicates}")

    def test_choice_values_are_valid(self):
        valid = {
            "light_needs": set(Plant.Light.values),
            "humidity_needs": set(Plant.Humidity.values),
            "care_difficulty": set(Plant.CareDifficulty.values),
            "water_frequency": set(Plant.WaterFrequency.values),
        }
        category_slugs = {category["slug"] for category in CATEGORIES}
        for plant in PLANTS:
            for field, allowed in valid.items():
                self.assertIn(plant[field], allowed, f"{plant['name']}: {field}")
            self.assertIn(plant["category"], category_slugs, plant["name"])

    def test_temperature_ranges_and_heights_are_sane(self):
        for plant in PLANTS:
            self.assertLessEqual(plant["temp_min"], plant["temp_max"], plant["name"])
            self.assertGreaterEqual(plant["max_height"], 1, plant["name"])

    def test_every_category_has_plants(self):
        used = {plant["category"] for plant in PLANTS}
        for category in CATEGORIES:
            self.assertIn(category["slug"], used, f"Пустая категория: {category['slug']}")

    def test_image_slugs_are_unique(self):
        slugs = [plant["image_slug"] for plant in PLANTS]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_plant_ships_with_a_photo(self):
        for plant in PLANTS:
            photo = SEED_IMAGES_DIR / f"{plant['image_slug']}.jpg"
            self.assertTrue(photo.exists(), f"Нет фото: {plant['name']}")


class CatalogueViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = PlantCategory.objects.create(name="Суккуленты", slug="succulents")
        cls.safe = Plant.objects.create(
            name="Эхеверия", scientific_name="Echeveria", category=cls.category,
            light_needs="bright", humidity_needs="low", temp_min=10, temp_max=27,
            toxicity=False, care_difficulty="easy", water_frequency="rare", max_height=15,
        )
        cls.toxic = Plant.objects.create(
            name="Алоэ", scientific_name="Aloe vera", category=cls.category,
            light_needs="bright", humidity_needs="low", temp_min=13, temp_max=30,
            toxicity=True, care_difficulty="easy", water_frequency="rare", max_height=60,
        )

    def test_list_page_loads(self):
        response = self.client.get(reverse("catalog:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Эхеверия")

    def test_detail_page_loads(self):
        response = self.client.get(reverse("catalog:detail", args=[self.safe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Echeveria")

    def test_search_filters_by_name(self):
        response = self.client.get(reverse("catalog:list"), {"q": "Алоэ"})
        self.assertContains(response, "Алоэ")
        self.assertNotContains(response, "Эхеверия")

    def test_pet_safe_filter_excludes_toxic(self):
        response = self.client.get(reverse("catalog:list"), {"pet_safe": "on"})
        self.assertContains(response, "Эхеверия")
        self.assertNotContains(response, "Алоэ")
