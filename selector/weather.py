"""Open-Meteo integration.

Resolves a city name to coordinates (Open-Meteo geocoding API) and reads the
current temperature and relative humidity (Open-Meteo forecast API). Both APIs
are free and keyless, so there are no secrets to configure. The relative
humidity percentage is mapped onto the room humidity scale used by the form.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10  # seconds


class WeatherError(Exception):
    """Raised when the weather data cannot be retrieved."""


@dataclass
class WeatherSnapshot:
    place: str
    temperature: int
    humidity_percent: int
    humidity_level: str  # one of RoomCondition.Humidity values


def humidity_to_level(percent: float) -> str:
    """Map a relative humidity percentage onto the room humidity scale."""
    if percent < 40:
        return "low"
    if percent < 70:
        return "medium"
    return "high"


def geocode_city(city: str) -> tuple[float, float, str]:
    """Return (latitude, longitude, resolved name) for a city name."""
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "ru", "format": "json"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        results = response.json().get("results") or []
    except requests.RequestException as exc:
        raise WeatherError("Не удалось связаться с сервисом геокодирования.") from exc
    except ValueError as exc:  # invalid JSON
        raise WeatherError("Сервис погоды вернул некорректный ответ.") from exc

    if not results:
        raise WeatherError(f"Город «{city}» не найден.")

    top = results[0]
    name_parts = [top.get("name"), top.get("country")]
    place = ", ".join(part for part in name_parts if part)
    return top["latitude"], top["longitude"], place


def fetch_current_weather(city: str) -> WeatherSnapshot:
    """Fetch the current temperature and humidity for a city."""
    latitude, longitude, place = geocode_city(city)
    try:
        response = requests.get(
            FORECAST_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m",
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        current = response.json()["current"]
        temperature = round(current["temperature_2m"])
        humidity_percent = round(current["relative_humidity_2m"])
    except requests.RequestException as exc:
        raise WeatherError("Не удалось получить данные о погоде.") from exc
    except (KeyError, ValueError, TypeError) as exc:
        raise WeatherError("Сервис погоды вернул неполные данные.") from exc

    return WeatherSnapshot(
        place=place,
        temperature=temperature,
        humidity_percent=humidity_percent,
        humidity_level=humidity_to_level(humidity_percent),
    )
