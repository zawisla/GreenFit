from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class PlantCategory(models.Model):
    """A grouping of plants, e.g. "Суккуленты" or "Папоротники"."""

    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("URL-идентификатор", max_length=120, unique=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Категория растений"
        verbose_name_plural = "Категории растений"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Plant(models.Model):
    """A single indoor plant with its care requirements."""

    class Light(models.TextChoices):
        LOW = "low", "Тень / слабый свет"
        MEDIUM = "medium", "Рассеянный свет"
        BRIGHT = "bright", "Яркий свет"

    class Humidity(models.TextChoices):
        LOW = "low", "Низкая"
        MEDIUM = "medium", "Средняя"
        HIGH = "high", "Высокая"

    class CareDifficulty(models.TextChoices):
        EASY = "easy", "Лёгкий"
        MEDIUM = "medium", "Средний"
        HARD = "hard", "Сложный"

    class WaterFrequency(models.TextChoices):
        RARE = "rare", "Редкий"
        REGULAR = "regular", "Регулярный"
        FREQUENT = "frequent", "Частый"

    name = models.CharField("Название", max_length=150)
    scientific_name = models.CharField("Научное название", max_length=150, blank=True)
    category = models.ForeignKey(
        PlantCategory,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="plants",
    )
    light_needs = models.CharField(
        "Потребность в свете", max_length=10, choices=Light.choices
    )
    humidity_needs = models.CharField(
        "Потребность во влажности", max_length=10, choices=Humidity.choices
    )
    temp_min = models.IntegerField("Минимальная температура, °C")
    temp_max = models.IntegerField("Максимальная температура, °C")
    toxicity = models.BooleanField("Токсично для животных", default=False)
    care_difficulty = models.CharField(
        "Сложность ухода", max_length=10, choices=CareDifficulty.choices
    )
    water_frequency = models.CharField(
        "Частота полива", max_length=10, choices=WaterFrequency.choices
    )
    max_height = models.IntegerField(
        "Максимальная высота, см", validators=[MinValueValidator(1)]
    )
    image = models.ImageField("Фото", upload_to="plants/", blank=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Растение"
        verbose_name_plural = "Растения"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=Q(temp_min__lte=F("temp_max")),
                name="catalog_plant_temp_range_valid",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def temperature_range(self) -> str:
        return f"{self.temp_min}…{self.temp_max} °C"

    @property
    def is_pet_safe(self) -> bool:
        return not self.toxicity
