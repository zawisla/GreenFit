from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .weather import WeatherError, fetch_current_weather


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
