from django.conf import settings
from django.db import models


class RoomCondition(models.Model):
    """The six microclimate parameters of a room entered by a user.

    The light/humidity choices intentionally mirror the matching scale used by
    :class:`catalog.models.Plant` so the two can be compared directly by the
    matching engine.
    """

    class Light(models.TextChoices):
        LOW = "low", "Тёмное помещение"
        MEDIUM = "medium", "Среднее освещение"
        BRIGHT = "bright", "Яркое освещение"

    class Humidity(models.TextChoices):
        LOW = "low", "Сухой воздух"
        MEDIUM = "medium", "Нормальная влажность"
        HIGH = "high", "Влажный воздух"

    class RoomSize(models.TextChoices):
        SMALL = "small", "Маленькое"
        MEDIUM = "medium", "Среднее"
        LARGE = "large", "Большое"

    class CareTime(models.TextChoices):
        MINIMAL = "minimal", "Минимум времени"
        AVERAGE = "average", "Умеренно"
        MUCH = "much", "Много времени"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="room_conditions",
    )
    light_level = models.CharField("Освещённость", max_length=10, choices=Light.choices)
    humidity = models.CharField("Влажность", max_length=10, choices=Humidity.choices)
    temperature = models.IntegerField("Температура, °C")
    room_size = models.CharField(
        "Размер помещения", max_length=10, choices=RoomSize.choices
    )
    has_pets = models.BooleanField("Есть домашние животные", default=False)
    care_time = models.CharField(
        "Свободное время на уход", max_length=10, choices=CareTime.choices
    )
    created_at = models.DateTimeField("Дата подбора", auto_now_add=True)

    class Meta:
        verbose_name = "Параметры помещения"
        verbose_name_plural = "Параметры помещений"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Помещение #{self.pk} ({self.get_light_level_display()}, {self.temperature} °C)"


class MatchResult(models.Model):
    """A single plant scored against one set of room conditions."""

    room = models.ForeignKey(
        RoomCondition,
        verbose_name="Помещение",
        on_delete=models.CASCADE,
        related_name="results",
    )
    plant = models.ForeignKey(
        "catalog.Plant",
        verbose_name="Растение",
        on_delete=models.CASCADE,
        related_name="match_results",
    )
    match_score = models.FloatField("Совместимость, %")
    reasons = models.TextField("Пояснения", blank=True)

    class Meta:
        verbose_name = "Результат подбора"
        verbose_name_plural = "Результаты подбора"
        ordering = ["-match_score"]

    def __str__(self) -> str:
        return f"{self.plant} — {self.match_score:.0f}%"

    @property
    def reason_lines(self) -> list[str]:
        """The stored explanations split into individual lines for templates."""
        return [line for line in self.reasons.splitlines() if line.strip()]
