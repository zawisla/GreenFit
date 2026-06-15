"""Populate the catalogue with demonstration categories and plants.

Run with::

    python manage.py seed_plants          # add / update demo data
    python manage.py seed_plants --clear   # wipe catalogue first

The data is intentionally varied (toxic and pet-safe species, every light and
humidity level, heights from 15 to 250 cm) so the matching engine and the
statistics page have something meaningful to show.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Plant, PlantCategory

CATEGORIES = [
    {"name": "Суккуленты", "slug": "succulents",
     "description": "Засухоустойчивые растения, запасающие влагу в листьях и стеблях."},
    {"name": "Декоративно-лиственные", "slug": "foliage",
     "description": "Растения, ценные своей декоративной листвой."},
    {"name": "Цветущие", "slug": "flowering",
     "description": "Красивоцветущие комнатные растения."},
    {"name": "Лианы и ампельные", "slug": "vines",
     "description": "Вьющиеся и свисающие растения."},
    {"name": "Папоротники", "slug": "ferns",
     "description": "Влаголюбивые папоротники с ажурными листьями."},
    {"name": "Пальмы", "slug": "palms",
     "description": "Комнатные пальмы, создающие уют."},
    {"name": "Деревья", "slug": "trees",
     "description": "Комнатные деревья и крупные одревесневающие растения."},
]

PLANTS = [
    {"name": "Сансевиерия трёхполосная", "scientific_name": "Sansevieria trifasciata",
     "category": "succulents", "light_needs": "low", "humidity_needs": "low",
     "temp_min": 15, "temp_max": 30, "toxicity": True, "care_difficulty": "easy",
     "water_frequency": "rare", "max_height": 90,
     "description": "Неприхотливое растение с жёсткими вертикальными листьями. Прощает редкий полив и тень."},
    {"name": "Замиокулькас", "scientific_name": "Zamioculcas zamiifolia",
     "category": "foliage", "light_needs": "low", "humidity_needs": "low",
     "temp_min": 16, "temp_max": 30, "toxicity": True, "care_difficulty": "easy",
     "water_frequency": "rare", "max_height": 100,
     "description": "Глянцевые перистые листья, накапливает влагу в корнях. Идеален для занятых владельцев."},
    {"name": "Спатифиллум", "scientific_name": "Spathiphyllum wallisii",
     "category": "flowering", "light_needs": "low", "humidity_needs": "high",
     "temp_min": 18, "temp_max": 28, "toxicity": True, "care_difficulty": "medium",
     "water_frequency": "frequent", "max_height": 60,
     "description": "«Женское счастье» с белыми соцветиями. Любит влажный воздух и регулярный полив."},
    {"name": "Калатея", "scientific_name": "Calathea orbifolia",
     "category": "foliage", "light_needs": "low", "humidity_needs": "high",
     "temp_min": 18, "temp_max": 26, "toxicity": False, "care_difficulty": "hard",
     "water_frequency": "frequent", "max_height": 60,
     "description": "Эффектные узорчатые листья, складывающиеся на ночь. Требовательна к влажности."},
    {"name": "Эпипремнум золотистый", "scientific_name": "Epipremnum aureum",
     "category": "vines", "light_needs": "medium", "humidity_needs": "medium",
     "temp_min": 17, "temp_max": 30, "toxicity": True, "care_difficulty": "easy",
     "water_frequency": "regular", "max_height": 200,
     "description": "Быстрорастущая лиана с пёстрой листвой. Хорошо очищает воздух."},
    {"name": "Нефролепис возвышенный", "scientific_name": "Nephrolepis exaltata",
     "category": "ferns", "light_needs": "medium", "humidity_needs": "high",
     "temp_min": 16, "temp_max": 24, "toxicity": False, "care_difficulty": "medium",
     "water_frequency": "frequent", "max_height": 70,
     "description": "Пышный папоротник с ажурными вайями. Нуждается в высокой влажности."},
    {"name": "Орхидея фаленопсис", "scientific_name": "Phalaenopsis",
     "category": "flowering", "light_needs": "medium", "humidity_needs": "high",
     "temp_min": 18, "temp_max": 28, "toxicity": False, "care_difficulty": "medium",
     "water_frequency": "regular", "max_height": 70,
     "description": "Долгоцветущая орхидея с эффектными цветками. Любит рассеянный свет."},
    {"name": "Хамедорея изящная", "scientific_name": "Chamaedorea elegans",
     "category": "palms", "light_needs": "medium", "humidity_needs": "medium",
     "temp_min": 18, "temp_max": 27, "toxicity": False, "care_difficulty": "medium",
     "water_frequency": "regular", "max_height": 180,
     "description": "Компактная комнатная пальма, теневынослива и безопасна для животных."},
    {"name": "Драцена окаймлённая", "scientific_name": "Dracaena marginata",
     "category": "foliage", "light_needs": "medium", "humidity_needs": "medium",
     "temp_min": 18, "temp_max": 28, "toxicity": True, "care_difficulty": "easy",
     "water_frequency": "regular", "max_height": 200,
     "description": "Стройное растение с узкими листьями на тонком стволе. Очень неприхотлива."},
    {"name": "Монстера деликатесная", "scientific_name": "Monstera deliciosa",
     "category": "vines", "light_needs": "medium", "humidity_needs": "medium",
     "temp_min": 18, "temp_max": 29, "toxicity": True, "care_difficulty": "medium",
     "water_frequency": "regular", "max_height": 250,
     "description": "Крупная лиана с резными листьями. Эффектный акцент для просторных комнат."},
    {"name": "Хлорофитум хохлатый", "scientific_name": "Chlorophytum comosum",
     "category": "foliage", "light_needs": "bright", "humidity_needs": "medium",
     "temp_min": 15, "temp_max": 27, "toxicity": False, "care_difficulty": "easy",
     "water_frequency": "regular", "max_height": 40,
     "description": "Классическое растение с дугообразными листьями и «детками». Растёт почти везде."},
    {"name": "Фикус Бенджамина", "scientific_name": "Ficus benjamina",
     "category": "trees", "light_needs": "bright", "humidity_needs": "medium",
     "temp_min": 18, "temp_max": 28, "toxicity": True, "care_difficulty": "medium",
     "water_frequency": "regular", "max_height": 200,
     "description": "Деревце с мелкими глянцевыми листьями. Любит яркий рассеянный свет."},
    {"name": "Алоэ вера", "scientific_name": "Aloe vera",
     "category": "succulents", "light_needs": "bright", "humidity_needs": "low",
     "temp_min": 13, "temp_max": 30, "toxicity": True, "care_difficulty": "easy",
     "water_frequency": "rare", "max_height": 60,
     "description": "Суккулент с целебным соком. Накапливает влагу, требует яркого света."},
    {"name": "Эхеверия изящная", "scientific_name": "Echeveria elegans",
     "category": "succulents", "light_needs": "bright", "humidity_needs": "low",
     "temp_min": 10, "temp_max": 27, "toxicity": False, "care_difficulty": "easy",
     "water_frequency": "rare", "max_height": 15,
     "description": "Розетка из плотных листьев, миниатюрный суккулент для подоконника."},
    {"name": "Эхинопсис", "scientific_name": "Echinopsis",
     "category": "succulents", "light_needs": "bright", "humidity_needs": "low",
     "temp_min": 10, "temp_max": 35, "toxicity": False, "care_difficulty": "easy",
     "water_frequency": "rare", "max_height": 30,
     "description": "Шаровидный кактус, цветущий крупными цветками. Минимальный уход."},
]


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
