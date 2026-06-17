from django.test import SimpleTestCase

from catalog.models import Plant
from catalog.plant_data import CATEGORIES, PLANTS


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
