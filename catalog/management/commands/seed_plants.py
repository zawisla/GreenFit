"""Populate the catalogue with demonstration categories and plants.

Run with::

    python manage.py seed_plants          # add / update demo data
    python manage.py seed_plants --clear   # wipe catalogue first

The plant data lives in :mod:`catalog.plant_data`. Every record is validated
against the model choices before anything is written, so a typo in the data
fails loudly instead of producing a broken catalogue.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Plant, PlantCategory
from catalog.plant_data import CATEGORIES, PLANTS

# Plant fields whose values must stay within the model's choices.
CHOICE_FIELDS = {
    "light_needs": Plant.Light,
    "humidity_needs": Plant.Humidity,
    "care_difficulty": Plant.CareDifficulty,
    "water_frequency": Plant.WaterFrequency,
}


def validate_catalogue(category_slugs):
    """Validate every plant record, collecting all problems before raising."""
    errors = []
    seen_names = set()
    for plant in PLANTS:
        name = plant.get("name", "<без названия>")
        if name in seen_names:
            errors.append(f"Дубликат названия: {name}")
        seen_names.add(name)
        for field, choices in CHOICE_FIELDS.items():
            if plant[field] not in choices.values:
                errors.append(f"{name}: недопустимое {field}={plant[field]!r}")
        if plant["category"] not in category_slugs:
            errors.append(f"{name}: неизвестная категория {plant['category']!r}")
        if plant["temp_min"] > plant["temp_max"]:
            errors.append(f"{name}: temp_min ({plant['temp_min']}) > temp_max ({plant['temp_max']})")
        if plant["max_height"] < 1:
            errors.append(f"{name}: высота должна быть положительной")
    if errors:
        raise CommandError("Ошибки в данных каталога:\n  " + "\n  ".join(errors))


class Command(BaseCommand):
    help = "Заполняет каталог демонстрационными категориями и растениями."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить существующие растения и категории перед заполнением.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        category_slugs = {category["slug"] for category in CATEGORIES}
        validate_catalogue(category_slugs)

        if options["clear"]:
            Plant.objects.all().delete()
            PlantCategory.objects.all().delete()
            self.stdout.write("Каталог очищен.")

        categories = {}
        for data in CATEGORIES:
            category, _ = PlantCategory.objects.update_or_create(
                slug=data["slug"],
                defaults={"name": data["name"], "description": data["description"]},
            )
            categories[data["slug"]] = category

        created = 0
        for data in PLANTS:
            payload = dict(data)
            category = categories[payload.pop("category")]
            _, was_created = Plant.objects.update_or_create(
                name=payload["name"],
                defaults={**payload, "category": category},
            )
            created += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: {len(categories)} категорий, {len(PLANTS)} растений "
                f"(добавлено новых: {created})."
            )
        )
