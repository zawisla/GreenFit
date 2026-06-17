from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from catalog.models import Plant, PlantCategory

from .analytics import build_statistics
from .forms import RoomConditionForm
from .matching import rank_plants
from .models import MatchResult, RoomCondition
from .weather import WeatherError, fetch_current_weather

# How many ranked plants to display on the result page. Every plant is still
# scored and stored; this only limits how many cards are rendered.
RESULT_DISPLAY_LIMIT = 30


def home(request):
    """Landing page with a short pitch and catalogue size."""
    context = {
        "plant_count": Plant.objects.count(),
        "category_count": PlantCategory.objects.count(),
        "safe_count": Plant.objects.filter(toxicity=False).count(),
    }
    return render(request, "selector/home.html", context)


def select(request):
    """Show the room form and, on submit, compute and persist the matches."""
    if request.method == "POST":
        form = RoomConditionForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            if request.user.is_authenticated:
                room.user = request.user
            room.save()

            plants = Plant.objects.select_related("category")
            matches = rank_plants(room, plants)
            MatchResult.objects.bulk_create(
                [
                    MatchResult(
                        room=room,
                        plant=match.plant,
                        match_score=match.score,
                        reasons=match.reasons_text,
                    )
                    for match in matches
                ]
            )
            return redirect("selector:result", pk=room.pk)
    else:
        form = RoomConditionForm()
    return render(request, "selector/select.html", {"form": form})


def result(request, pk):
    """Ranked compatibility list with per-criterion explanations."""
    room = get_object_or_404(RoomCondition, pk=pk)
    # A saved (user-owned) selection is private to its owner; guest selections
    # (user is None) remain viewable by link.
    if room.user_id and room.user_id != request.user.id:
        raise Http404("Подбор не найден.")

    plants = Plant.objects.select_related("category")
    matches = rank_plants(room, plants)

    # Optional filters narrow the ranked list without changing the scoring.
    pet_safe = request.GET.get("pet_safe") == "on"
    easy_only = request.GET.get("easy") == "on"
    category = (request.GET.get("category") or "").strip()
    if pet_safe:
        matches = [m for m in matches if not m.plant.toxicity]
    if easy_only:
        matches = [m for m in matches if m.plant.care_difficulty == Plant.CareDifficulty.EASY]
    if category:
        matches = [m for m in matches if m.plant.category.slug == category]

    context = {
        "room": room,
        "matches": matches[:RESULT_DISPLAY_LIMIT],
        "shown": min(len(matches), RESULT_DISPLAY_LIMIT),
        "total": len(matches),
        "categories": PlantCategory.objects.all(),
        "pet_safe": pet_safe,
        "easy": easy_only,
        "active_category": category,
    }
    return render(request, "selector/result.html", context)


def statistics(request):
    """Aggregate statistics over all recorded matches (Pandas)."""
    return render(request, "selector/statistics.html", {"stats": build_statistics()})


@login_required
def history(request):
    """List the authenticated user's past selections, best match first."""
    rooms = (
        RoomCondition.objects.filter(user=request.user)
        .prefetch_related("results__plant")
    )
    return render(request, "selector/history.html", {"rooms": rooms})


@require_GET
def weather_api(request):
    """AJAX endpoint: return current weather for a city to prefill the form."""
    city = (request.GET.get("city") or "").strip()
    if not city:
        return JsonResponse({"error": "Укажите город."}, status=400)
    try:
        snapshot = fetch_current_weather(city)
    except WeatherError as exc:
        return JsonResponse({"error": str(exc)}, status=502)
    return JsonResponse(
        {
            "place": snapshot.place,
            "temperature": snapshot.temperature,
            "humidity_percent": snapshot.humidity_percent,
            "humidity_level": snapshot.humidity_level,
        }
    )
