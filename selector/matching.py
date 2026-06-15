"""Compatibility engine for GreenFit.

Given a :class:`~selector.models.RoomCondition` and a set of
:class:`~catalog.models.Plant` objects, this module scores how well each plant
fits the room across six weighted criteria and produces a human-readable
explanation for every criterion. It performs no database access, which keeps
the business logic isolated from the views and trivial to unit-test.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Relative importance of each criterion. The weights sum to 100 so that the
# final compatibility score is a percentage.
WEIGHTS = {
    "light": 25,
    "temperature": 20,
    "care": 20,
    "pets": 15,
    "humidity": 10,
    "size": 10,
}

# Ordinal scales shared between rooms and plants.
LIGHT_ORDER = {"low": 0, "medium": 1, "bright": 2}
HUMIDITY_ORDER = {"low": 0, "medium": 1, "high": 2}
CARE_TIME_ORDER = {"minimal": 0, "average": 1, "much": 2}
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}
WATER_ORDER = {"rare": 0, "regular": 1, "frequent": 2}

# Comfortable / maximum plant height (cm) for each room size.
ROOM_SIZE_HEIGHT = {
    "small": {"ideal": 40, "max": 70},
    "medium": {"ideal": 120, "max": 200},
    "large": {"ideal": 10_000, "max": 10_000},
}


@dataclass
class Criterion:
    """The outcome of scoring one criterion for one plant."""

    key: str
    label: str
    weight: int
    fraction: float  # 0.0 .. 1.0 share of the weight that was awarded
    text: str

    @property
    def points(self) -> float:
        return round(self.fraction * self.weight, 1)

    @property
    def status(self) -> str:
        if self.fraction >= 0.8:
            return "good"
        if self.fraction >= 0.4:
            return "ok"
        return "bad"


@dataclass
class PlantMatch:
    """A plant together with its overall score and per-criterion breakdown."""

    plant: object
    score: float
    criteria: list[Criterion] = field(default_factory=list)

    @property
    def reasons_text(self) -> str:
        """Plain-text explanation persisted in ``MatchResult.reasons``."""
        return "\n".join(f"{c.label}: {c.text}" for c in self.criteria)

    @property
    def status(self) -> str:
        if self.score >= 75:
            return "good"
        if self.score >= 50:
            return "ok"
        return "bad"


def _ordinal_fraction(a: int, b: int, max_distance: int = 2) -> float:
    """Linear closeness of two ordinal values (1.0 when equal, 0.0 when farthest)."""
    return max(0.0, 1.0 - abs(a - b) / max_distance)


def _score_light(room, plant) -> Criterion:
    fraction = _ordinal_fraction(
        LIGHT_ORDER[room.light_level], LIGHT_ORDER[plant.light_needs]
    )
    plant_need = plant.get_light_needs_display().lower()
    room_has = room.get_light_level_display().lower()
    if fraction >= 0.99:
        text = f"Освещение подходит идеально: растению нужен {plant_need}, и в помещении {room_has}."
    elif fraction >= 0.4:
        text = f"Освещение отличается на один уровень: растению нужен {plant_need}, а у вас {room_has}."
    else:
        text = f"Сильное несоответствие по свету: растению нужен {plant_need}, а помещение — {room_has}."
    return Criterion("light", "Освещение", WEIGHTS["light"], fraction, text)


def _score_humidity(room, plant) -> Criterion:
    fraction = _ordinal_fraction(
        HUMIDITY_ORDER[room.humidity], HUMIDITY_ORDER[plant.humidity_needs]
    )
    plant_need = plant.get_humidity_needs_display().lower()
    room_has = room.get_humidity_display().lower()
    if fraction >= 0.99:
        text = f"Влажность подходит: растению нужна {plant_need} влажность, в помещении {room_has}."
    elif fraction >= 0.4:
        text = f"Влажность отличается на один уровень: растению нужна {plant_need}, а у вас {room_has}."
    else:
        text = f"Сильное несоответствие по влажности: растению нужна {plant_need}, а в помещении {room_has}."
    return Criterion("humidity", "Влажность", WEIGHTS["humidity"], fraction, text)


def _score_temperature(room, plant) -> Criterion:
    t = room.temperature
    if plant.temp_min <= t <= plant.temp_max:
        fraction = 1.0
        text = (
            f"Температура {t} °C находится в комфортном диапазоне "
            f"{plant.temp_min}…{plant.temp_max} °C."
        )
    elif t < plant.temp_min:
        delta = plant.temp_min - t
        fraction = max(0.0, 1.0 - delta / 10)
        text = (
            f"В помещении {t} °C — на {delta} °C холоднее минимума "
            f"{plant.temp_min} °C для этого растения."
        )
    else:
        delta = t - plant.temp_max
        fraction = max(0.0, 1.0 - delta / 10)
        text = (
            f"В помещении {t} °C — на {delta} °C жарче максимума "
            f"{plant.temp_max} °C для этого растения."
        )
    return Criterion("temperature", "Температура", WEIGHTS["temperature"], fraction, text)


def _score_size(room, plant) -> Criterion:
    bounds = ROOM_SIZE_HEIGHT[room.room_size]
    height = plant.max_height
    if room.room_size == "large":
        fraction = 1.0
        text = "Большое помещение вместит растение любого размера."
    elif height <= bounds["ideal"]:
        fraction = 1.0
        text = f"Высота до {height} см хорошо подходит для выбранного размера помещения."
    elif height <= bounds["max"]:
        span = bounds["max"] - bounds["ideal"]
        fraction = round(1.0 - 0.6 * (height - bounds["ideal"]) / span, 2)
        text = f"Растение может вырасти до {height} см — для такого помещения это уже крупновато."
    else:
        fraction = 0.2
        text = f"Растение вырастает до {height} см и будет слишком большим для этого помещения."
    return Criterion("size", "Размер", WEIGHTS["size"], fraction, text)


def _score_pets(room, plant) -> Criterion:
    if not room.has_pets:
        fraction = 1.0
        text = "В доме нет животных — токсичность растения не имеет значения."
    elif plant.toxicity:
        fraction = 0.0
        text = "⚠️ Растение токсично для животных, а у вас есть питомцы — будьте осторожны."
    else:
        fraction = 1.0
        text = "Растение безопасно для домашних животных."
    return Criterion("pets", "Безопасность для животных", WEIGHTS["pets"], fraction, text)


def _score_care(room, plant) -> Criterion:
    capacity = CARE_TIME_ORDER[room.care_time]
    demand = (DIFFICULTY_ORDER[plant.care_difficulty] + WATER_ORDER[plant.water_frequency]) / 2
    difficulty = plant.get_care_difficulty_display().lower()
    watering = plant.get_water_frequency_display().lower()
    available = room.get_care_time_display().lower()
    if capacity >= demand:
        fraction = 1.0
        text = (
            f"Уход по силам: сложность — {difficulty}, полив — {watering}, "
            f"а времени вы готовы уделять «{available}»."
        )
    else:
        gap = demand - capacity
        fraction = max(0.0, 1.0 - gap / 2)
        text = (
            f"Растению нужно больше внимания (сложность — {difficulty}, полив — {watering}), "
            f"чем вы планируете уделять («{available}»)."
        )
    return Criterion("care", "Уход", WEIGHTS["care"], fraction, text)


_SCORERS = (
    _score_light,
    _score_temperature,
    _score_care,
    _score_pets,
    _score_humidity,
    _score_size,
)


def match_plant(room, plant) -> PlantMatch:
    """Score a single plant against the room conditions."""
    criteria = [scorer(room, plant) for scorer in _SCORERS]
    score = round(sum(c.points for c in criteria), 1)
    return PlantMatch(plant=plant, score=score, criteria=criteria)


def rank_plants(room, plants) -> list[PlantMatch]:
    """Score every plant and return matches sorted from best to worst."""
    matches = [match_plant(room, plant) for plant in plants]
    matches.sort(key=lambda m: m.score, reverse=True)
    return matches
