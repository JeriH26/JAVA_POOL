# API Navigation with Python

**Estimated Time:** 35-60 minutes

You will use the Weather API (https://openweathermap.org/api) with Python to extract data from the Weather API and answer the following questions. You may need to use other APIs mentioned in the link to answer the questions.

If you cannot answer a question, just state that and move on to the next. If you can complete the bonus questions, great.

## Tasks

1. Create a Python function that outputs the differences in average daily forecast temperatures between zip codes `{city: 94203}` and `{city: 94102}` in Fahrenheit.

For all outputs, list the city name instead of the zip code (for example, `{city: 98039}` is Seattle).

A sample output would be:

`It is x degrees F colder in {city: 94203} on average than it is in {city: 94102} on August 23rd`

2. Create a Python function that outputs the differences in the hourly forecast temperatures between `{city: 94203}` and `{city: 94102}` in Celsius for the upcoming hour.

This will use the next hour from when it was called. For example, if it was called at 8:23 AM PT, it will start the forecast for both at 9:00 AM PT.

3. Create a Python function that outputs the combined values of both `{city: 94203}` and `{city: 94102}`:

- Combined average temperature during the day in Kelvin.
- Combined average humidity.
- Combined average cloudiness.

4. Bonus: With the outputs created in task (3), create an API document similar to the Weather API style and design.

5. Bonus: Create an API endpoint for the function outputs that matches the API document from task (4).

6. Bonus: Convert your API into a Docker service and deploy it.

## Submission Summary (Assisted by Github Copilot)

### What I built

- Implemented Python functions for tasks 1-3 in `starter.py`.
- Built REST endpoints for the same outputs using FastAPI in `api_app.py`.
- Wrote API-style documentation in `API_DOCUMENTATION.md`.
- Added Docker support with `Dockerfile`, `.dockerignore`, and `docker-compose.yml`.

### How to run

1. Install dependencies:

```bash
pip3 install -r requirements.txt
```

2. Configure the OpenWeather API key with `.env` (recommended):

Then edit `.env` and set your real key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Alternative (temporary shell variable):

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

3. Run as a local API service:

```bash
uvicorn api_app:app --reload --port 8000
```

Quick key health check (recommended before running full tasks):

```bash
python starter.py --check-key
```

4. Open docs:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

5. Optional Docker run:

```bash
docker build -t city-weather-api .
docker run --rm -p 8000:8000 -e OPENWEATHER_API_KEY="your_api_key_here" city-weather-api
```

### Known limitations

- Requires a valid OpenWeather API key.
- Forecast granularity depends on upstream API data availability.
- "Upcoming hour" uses the next full Pacific Time hour and matches against available forecast timestamps.
