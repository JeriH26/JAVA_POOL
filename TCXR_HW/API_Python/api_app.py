"""Bonus 4-5 implementation: API documentation aligned FastAPI endpoints.

Run:
    uvicorn api_app:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from starter import (
    WeatherApiError,
    average_daily_forecast_difference_fahrenheit,
    combined_city_metrics,
    upcoming_hour_difference_celsius,
)

app = FastAPI(
    title="City Weather Comparison API",
    description=(
        "Small API inspired by OpenWeather-style endpoint design. "
        "It compares forecast metrics between two ZIP codes."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/v1/temperature/daily-difference")
def daily_difference(
    zip_a: str = Query(default="94203", description="First ZIP code"),
    zip_b: str = Query(default="94102", description="Second ZIP code"),
) -> dict:
    """Task 1 endpoint: average daily forecast difference in Fahrenheit."""
    try:
        message = average_daily_forecast_difference_fahrenheit(zip_a, zip_b)
        return {
            "zip_a": zip_a,
            "zip_b": zip_b,
            "unit": "fahrenheit",
            "summary": message,
        }
    except WeatherApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/v1/temperature/next-hour-difference")
def next_hour_difference(
    zip_a: str = Query(default="94203", description="First ZIP code"),
    zip_b: str = Query(default="94102", description="Second ZIP code"),
) -> dict:
    """Task 2 endpoint: upcoming hour forecast difference in Celsius."""
    try:
        message = upcoming_hour_difference_celsius(zip_a, zip_b)
        return {
            "zip_a": zip_a,
            "zip_b": zip_b,
            "unit": "celsius",
            "summary": message,
        }
    except WeatherApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/v1/cities/combined-metrics")
def combined_metrics(
    zip_a: str = Query(default="94203", description="First ZIP code"),
    zip_b: str = Query(default="94102", description="Second ZIP code"),
) -> dict:
    """Task 3 endpoint: combined averages for temperature/humidity/cloudiness."""
    try:
        payload = combined_city_metrics(zip_a, zip_b)
        return {
            "zip_a": zip_a,
            "zip_b": zip_b,
            "unit_temperature": "kelvin",
            **payload,
        }
    except WeatherApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
