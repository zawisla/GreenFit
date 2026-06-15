from django.contrib import admin

from .models import MatchResult, RoomCondition


class MatchResultInline(admin.TabularInline):
    model = MatchResult
    extra = 0
    fields = ("plant", "match_score")
    readonly_fields = ("plant", "match_score")
    can_delete = False
    show_change_link = True


@admin.register(RoomCondition)
class RoomConditionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "light_level",
        "humidity",
        "temperature",
        "room_size",
        "has_pets",
        "care_time",
        "created_at",
    )
    list_filter = ("light_level", "humidity", "room_size", "care_time", "has_pets")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    inlines = (MatchResultInline,)


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ("plant", "room", "match_score")
    list_filter = ("plant__care_difficulty", "plant__category")
    search_fields = ("plant__name", "room__user__username")
    list_select_related = ("plant", "room")
