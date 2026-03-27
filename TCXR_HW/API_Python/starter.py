"""Starter implementation for: API Navigation with Python.

Setup:
1) export OPENWEATHER_API_KEY="your_api_key"
2) python3 starter.py
3) python3 starter.py --check-key   # quick API key health check
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import mean
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().with_name(".env"))

BASE_URL = "https://api.openweathermap.org"
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
PT_TZ = ZoneInfo("America/Los_Angeles")

ZIP_A = "94203"
ZIP_B = "94102"
COUNTRY_CODE = "US"


@dataclass
class Location:
    city: str
    lat: float
    lon: float


class WeatherApiError(RuntimeError):
    """Raised when OpenWeather request fails or response is incomplete."""


def _require_api_key() -> None:
    if not API_KEY:
        raise WeatherApiError(
            "OPENWEATHER_API_KEY is not set. Export it before running this script."
        )


def _get_json(path: str, params: dict) -> dict:
    _require_api_key()
    payload = {**params, "appid": API_KEY}
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, params=payload, timeout=20)
    if resp.status_code != 200:
        raise WeatherApiError(f"API request failed: {resp.status_code} {resp.text}")
    return resp.json()


def check_api_key_health() -> str:
    """Quick validation for OPENWEATHER_API_KEY without running full tasks."""
    _require_api_key()
    # Lightweight auth check using ZIP geocoding endpoint.
    resp = requests.get(
        f"{BASE_URL}/geo/1.0/zip",
        params={"zip": f"{ZIP_A},{COUNTRY_CODE}", "appid": API_KEY},
        timeout=20,
    )
    if resp.status_code == 200:
        return "API key is valid and active."
    if resp.status_code == 401:
        return (
            "API key is invalid or not activated yet (401). "
            "If you just created it, wait 10-30 minutes and retry."
        )
    return f"Unexpected API response: {resp.status_code} {resp.text}"


def resolve_zip_to_location(zip_code: str, country_code: str = COUNTRY_CODE) -> Location:
    """Resolve ZIP to city + coordinates using OpenWeather Geo API."""
    data = _get_json("/geo/1.0/zip", {"zip": f"{zip_code},{country_code}"})
    try:
        return Location(city=data["name"], lat=float(data["lat"]), lon=float(data["lon"]))
    except KeyError as exc:
        raise WeatherApiError(f"Missing field in ZIP lookup response: {exc}") from exc


def _get_5day_3hour_forecast(lat: float, lon: float, units: str) -> list[dict]:
    data = _get_json(
        "/data/2.5/forecast",
        {
            "lat": lat,
            "lon": lon,
            "units": units,
        },
    )
    items = data.get("list", [])
    if not items:
        raise WeatherApiError("Forecast response does not contain 'list' data.")
    return items


def _to_pt_from_unix(unix_ts: int) -> datetime:
    return datetime.fromtimestamp(unix_ts, tz=ZoneInfo("UTC")).astimezone(PT_TZ)


def _next_full_hour_pt(now_pt: datetime | None = None) -> datetime:
    now = now_pt or datetime.now(PT_TZ)
    return (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)


def average_daily_forecast_difference_fahrenheit(zip_a: str = ZIP_A, zip_b: str = ZIP_B) -> str:
    """Task 1: Difference in average daily forecast temp (Fahrenheit).

    Computes average temperature across all forecast points for the next full day
    (00:00-23:59 PT) for each ZIP's city, then returns human-readable difference.
    """
    loc_a = resolve_zip_to_location(zip_a)
    loc_b = resolve_zip_to_location(zip_b)

    forecast_a = _get_5day_3hour_forecast(loc_a.lat, loc_a.lon, units="imperial")
    forecast_b = _get_5day_3hour_forecast(loc_b.lat, loc_b.lon, units="imperial")

    target_date = (datetime.now(PT_TZ) + timedelta(days=1)).date()

    temps_a = [
        float(item["main"]["temp"])
        for item in forecast_a
        if _to_pt_from_unix(int(item["dt"])).date() == target_date
    ]
    temps_b = [
        float(item["main"]["temp"])
        for item in forecast_b
        if _to_pt_from_unix(int(item["dt"])).date() == target_date
    ]

    if not temps_a or not temps_b:
        raise WeatherApiError("Not enough forecast points to compute next-day averages.")

    avg_a = mean(temps_a)
    avg_b = mean(temps_b)
    diff = abs(avg_a - avg_b)

    if avg_a < avg_b:
        relation = "colder"
        city_left = loc_a.city
        city_right = loc_b.city
    else:
        relation = "warmer"
        city_left = loc_a.city
        city_right = loc_b.city

    day_label = target_date.strftime("%B %d")
    return (
        f"It is {diff:.2f} degrees F {relation} in {city_left} on average "
        f"than it is in {city_right} on {day_label}."
    )


def upcoming_hour_difference_celsius(zip_a: str = ZIP_A, zip_b: str = ZIP_B) -> str:
    """Task 2: Difference in hourly forecast temp (Celsius) for next full hour."""
    loc_a = resolve_zip_to_location(zip_a)
    loc_b = resolve_zip_to_location(zip_b)

    forecast_a = _get_5day_3hour_forecast(loc_a.lat, loc_a.lon, units="metric")
    forecast_b = _get_5day_3hour_forecast(loc_b.lat, loc_b.lon, units="metric")

    next_hour = _next_full_hour_pt()

    def get_temp_for_hour(items: list[dict]) -> tuple[float, datetime]:
        # Forecast is 3-hour intervals, so find the closest point to next_hour.
        closest = min(items, key=lambda item: abs(_to_pt_from_unix(int(item["dt"])) - next_hour))
        return float(closest["main"]["temp"]), _to_pt_from_unix(int(closest["dt"]))

    temp_a, actual_dt_a = get_temp_for_hour(forecast_a)
    temp_b, _ = get_temp_for_hour(forecast_b)
    diff = temp_a - temp_b

    return (
        f"At {actual_dt_a.strftime('%Y-%m-%d %H:%M %Z')} (nearest forecast point to {next_hour.strftime('%H:%M')}), "
        f"{loc_a.city} is {diff:+.2f} C compared to {loc_b.city}."
    )


def combined_city_metrics(zip_a: str = ZIP_A, zip_b: str = ZIP_B) -> dict:
    """Task 3: Combined metrics for both cities.

    Returns:
    - combined_avg_day_temp_kelvin
    - combined_avg_humidity
    - combined_avg_cloudiness
    """
    loc_a = resolve_zip_to_location(zip_a)
    loc_b = resolve_zip_to_location(zip_b)

    # Use /data/2.5/weather (current weather, free tier) instead of One Call 3.0.
    # No units param → temperature is returned in Kelvin by default.
    def current_weather(lat: float, lon: float) -> dict:
        return _get_json("/data/2.5/weather", {"lat": lat, "lon": lon})

    data_a = current_weather(loc_a.lat, loc_a.lon)
    data_b = current_weather(loc_b.lat, loc_b.lon)

    try:
        temp_k_avg = mean([float(data_a["main"]["temp"]), float(data_b["main"]["temp"])])
        humidity_avg = mean([float(data_a["main"]["humidity"]), float(data_b["main"]["humidity"])])
        clouds_avg = mean([float(data_a["clouds"]["all"]), float(data_b["clouds"]["all"])])
    except KeyError as exc:
        raise WeatherApiError(f"Missing expected current weather field: {exc}") from exc

    return {
        "cities": [loc_a.city, loc_b.city],
        "combined_avg_day_temp_kelvin": round(temp_k_avg, 2),
        "combined_avg_humidity": round(humidity_avg, 2),
        "combined_avg_cloudiness": round(clouds_avg, 2),
    }


def main() -> None:
    """Quick runner for tasks 1-3."""
    try:
        if "--check-key" in sys.argv:
            print(check_api_key_health())
            return

        print("Task 1:")
        print(average_daily_forecast_difference_fahrenheit())
        print()

        print("Task 2:")
        print(upcoming_hour_difference_celsius())
        print()

        print("Task 3:")
        print(combined_city_metrics())
    except WeatherApiError as err:
        print(f"Weather API error: {err}")


if __name__ == "__main__":
    main()
