# Absolute Humidity Calculator

A FastAPI web app that calculates absolute humidity (g/m³) from temperature and
relative humidity, using [PsychroLib](https://github.com/psychrometrics/psychrolib)
for ASHRAE-standard psychrometric calculations. It serves a small Jinja2 web
interface and a JSON API with automatic OpenAPI docs.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

```bash
uv sync            # install runtime dependencies
uv sync --dev      # also install dev/test dependencies
```

## Running

```bash
uv run python main.py
# or:  uv run uvicorn main:app --reload
```

Then visit:

- Web interface: http://localhost:8000
- API docs (Swagger UI): http://localhost:8000/docs

## API

### `POST /api/calculate`

Request:

```json
{ "temperature": 25.5, "humidity": 60 }
```

Response:

```json
{
    "absolute_humidity": 14.21,
    "temperature": 25.5,
    "humidity": 60,
    "unit": "g/m³"
}
```

```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25.5, "humidity": 60}'
```

Inputs are validated by Pydantic: `temperature` is in Celsius (−100 to 100) and
`humidity` is a percentage (0–100). Invalid inputs return `422`.

### `GET /api/health`

Returns `{ "status": "healthy" }`.

## Calculation

PsychroLib (SI units, standard atmospheric pressure of 101,325 Pa) computes the
humidity ratio and moist air density from temperature and relative humidity;
absolute humidity is their product, reported in g/m³ and rounded to 2 decimals.

## Development

```bash
uv sync --dev
uv run pytest
```

Calling the calculation directly:

```python
from app.psychro_calculations import calculate_absolute_humidity

print(calculate_absolute_humidity(25.0, 60))  # g/m³
```

### Project structure

```
abs_humidity_calc/
├── main.py                       # App factory, middleware, exception handlers
├── app/
│   ├── config.py                 # Configuration
│   ├── models.py                 # Pydantic request/response models
│   ├── psychro_calculations.py   # PsychroLib calculation
│   └── routes/
│       ├── api.py                # JSON API routes
│       └── web.py                # HTML routes
├── templates/                    # Jinja2 templates (base, index, about)
├── test_api.py                   # API tests
├── test_calculations.py          # Calculation tests
├── Dockerfile
└── pyproject.toml
```

## Deployment

The included `Dockerfile` builds a Cloud Run-ready image that serves the app with
uvicorn on port 8080.
