from django.contrib import admin
from django.db.models import Count

from .models import Plant, PlantCategory


@admin.register(PlantCategory)
class PlantCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "plant_count")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_plant_count=Count("plants"))

    @admin.display(description="Растений", ordering="_plant_count")
    def plant_count(self, obj):
        return obj._plant_count


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "scientific_name",
        "category",
        "light_needs",
        "humidity_needs",
        "care_difficulty",
        "water_frequency",
        "toxicity",
        "max_height",
    )
    list_filter = (
        "category",
        "light_needs",
        "humidity_needs",
        "care_difficulty",
        "water_frequency",
        "toxicity",
    )
    search_fields = ("name", "scientific_name", "description")
    list_select_related = ("category",)
    autocomplete_fields = ("category",)
    fieldsets = (
        (None, {"fields": ("name", "scientific_name", "category", "description", "image")}),
        (
            "Условия содержания",
            {
                "fields": (
                    "light_needs",
                    "humidity_needs",
                    ("temp_min", "temp_max"),
                    "water_frequency",
                    "care_difficulty",
                    "max_height",
                    "toxicity",
                )
            },
        ),
    )
