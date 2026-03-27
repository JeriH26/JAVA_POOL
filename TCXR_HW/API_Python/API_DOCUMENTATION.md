# City Weather Comparison API

Version: 1.0.0
Base URL: `http://localhost:8000`

This API is designed in a style similar to weather APIs: simple resource paths, clear units, and query-based filtering by ZIP code.

## Authentication

All endpoints require an environment variable on the server side:

- `OPENWEATHER_API_KEY`

No client token is required for local demo usage.

## Endpoints

### 1) GET `/health`

Purpose: quick service status check.

Response example:

```json
{
  "status": "ok"
}
```

### 2) GET `/v1/temperature/daily-difference`

Purpose: compare average daily forecast temperatures between two ZIP codes in Fahrenheit.

Query params:

- `zip_a` (string, default `94203`)
- `zip_b` (string, default `94102`)

Response example:

```json
{
  "zip_a": "94203",
  "zip_b": "94102",
  "unit": "fahrenheit",
  "summary": "It is 2.15 degrees F colder in Sacramento on average than it is in San Francisco on August 23."
}
```

### 3) GET `/v1/temperature/next-hour-difference`

Purpose: compare upcoming-hour forecast temperatures in Celsius.

Query params:

- `zip_a` (string, default `94203`)
- `zip_b` (string, default `94102`)

Response example:

```json
{
  "zip_a": "94203",
  "zip_b": "94102",
  "unit": "celsius",
  "summary": "At 2026-03-27 09:00 PDT, Sacramento is +1.20 C compared to San Francisco."
}
```

### 4) GET `/v1/cities/combined-metrics`

Purpose: return combined averages for the two cities.

Query params:

- `zip_a` (string, default `94203`)
- `zip_b` (string, default `94102`)

Response example:

```json
{
  "zip_a": "94203",
  "zip_b": "94102",
  "unit_temperature": "kelvin",
  "cities": [
    "Sacramento",
    "San Francisco"
  ],
  "combined_avg_day_temp_kelvin": 300.12,
  "combined_avg_humidity": 62.5,
  "combined_avg_cloudiness": 28.0
}
```

## Error Model

If upstream weather calls fail, the API returns HTTP 502.

Example:

```json
{
  "detail": "API request failed: 401 ..."
}
```

## Run Locally

```bash
cd API_Python
pip3 install -r requirements.txt
export OPENWEATHER_API_KEY="your_api_key_here"
uvicorn api_app:app --reload --port 8000
```

Open interactive docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Run with Docker

Build image:

```bash
cd API_Python
docker build -t city-weather-api .
```

Run container:

```bash
docker run --rm -p 8000:8000 \
  -e OPENWEATHER_API_KEY="your_api_key_here" \
  city-weather-api
```

Or run with Docker Compose:

```bash
cd API_Python
export OPENWEATHER_API_KEY="your_api_key_here"
docker compose up --build
```

Then open:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment Notes

This container can be deployed to any container platform (for example: Render, Railway, Fly.io, ECS, GCP Cloud Run, or Azure Container Apps).

Required runtime variable:

- `OPENWEATHER_API_KEY`
