# Absolute Humidity Calculator

A modern FastAPI web application that calculates absolute humidity from temperature and relative humidity inputs, featuring a beautiful Jinja2-templated web interface and comprehensive REST API.

## Features

- **Modern FastAPI backend** with automatic API documentation
- **Beautiful web interface** built with Jinja2 templates and responsive design
- **REST API** with automatic validation using Pydantic models
- **Comprehensive testing** with pytest (65+ test cases)
- **Input validation** and error handling
- **Interactive API documentation** (Swagger UI and ReDoc)
- **Health check endpoints**
- **Type hints** and modern Python practices

## Installation

This project uses UV for dependency management. Make sure you have UV installed.

1. Install dependencies:
```bash
uv sync
```

2. Install development dependencies (for testing):
```bash
uv sync --extra dev
```

## Usage

### Running the Application

Start the FastAPI server:
```bash
uv run python main.py
```

The application will be available at:
- **Web Interface**: `http://localhost:8000`
- **API Documentation (Swagger)**: `http://localhost:8000/docs`
- **API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter temperature in Celsius (decimal values allowed)
3. Enter relative humidity as a percentage (0-100)
4. Click "Calculate Absolute Humidity" to get the result
5. Try the quick example buttons for common scenarios

### API Usage

#### Calculate Absolute Humidity

**Endpoint:** `POST /api/calculate`

**Request Body:**
```json
{
    "temperature": 25.5,
    "humidity": 60
}
```

**Response:**
```json
{
    "absolute_humidity": 14.21,
    "temperature": 25.5,
    "humidity": 60,
    "unit": "g/m³"
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25.5, "humidity": 60}'
```

#### Health Check

**Endpoints:** 
- `GET /api/health`
- `GET /health` (alternative)

**Response:**
```json
{
    "status": "healthy"
}
```

## Parameters

- **Temperature**: Float value in Celsius (e.g., 25.5)
- **Humidity**: Integer value representing relative humidity percentage (0-100)

## Formula

The application uses the Magnus formula to calculate saturation vapor pressure and then determines absolute humidity using the ideal gas law:

1. **Saturation vapor pressure**: `es = 6.112 * exp((17.67 * T) / (T + 243.5))`
2. **Actual vapor pressure**: `e = (RH/100) * es`
3. **Absolute humidity**: `AH = (e * 18.016) / (8314.5 * (T + 273.15)) * 1000`

Where:
- T = temperature in Celsius
- RH = relative humidity in percent
- es = saturation vapor pressure in hPa
- e = actual vapor pressure in hPa
- AH = absolute humidity in g/m³

## Error Handling

The API returns appropriate HTTP status codes and error messages for:
- Missing or invalid input parameters (422 Unprocessable Entity)
- Out-of-range humidity values (0-100)
- Invalid JSON format
- Type validation errors
- Server errors (500 Internal Server Error)

## Development

### Project Structure

```
abs_humidity_calc/
├── main.py                 # FastAPI application
├── templates/
│   └── index.html         # Jinja2 template for web interface
├── test_calculations.py   # Unit tests for calculations
├── test_api.py           # Integration tests for API
├── example_usage.py      # Usage examples
├── pytest.ini           # Pytest configuration
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

### Running Tests

This project uses pytest for testing with comprehensive coverage:

```bash
# Install dev dependencies first
uv sync --extra dev

# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test files
uv run pytest test_calculations.py -v
uv run pytest test_api.py -v

# Run tests with coverage
uv add --dev coverage
uv run coverage run -m pytest
uv run coverage report
```

### Test Coverage

**Calculation Tests (21 tests):**
- Standard conditions testing
- Edge cases (0%, 100% humidity, negative temperatures)
- Parametrized tests for various conditions
- Type and precision validation
- Extreme weather conditions

**API Tests (44 tests):**
- Health endpoint testing
- Web interface validation
- Successful calculation scenarios
- Comprehensive error handling
- HTTP method restrictions
- Response format validation
- API documentation endpoints
- Live server integration tests

### FastAPI Features

This application leverages modern FastAPI features:

- **Automatic API documentation** with Swagger UI and ReDoc
- **Pydantic models** for request/response validation
- **Type hints** throughout the codebase
- **Dependency injection** ready for future enhancements
- **Async support** for scalability
- **Modern Python practices** (3.11+)

### UV Commands

- **Install dependencies**: `uv sync`
- **Install dev dependencies**: `uv sync --extra dev`
- **Run the app**: `uv run python main.py`
- **Run tests**: `uv run pytest`
- **Add new dependencies**: `uv add package_name`
- **Add dev dependencies**: `uv add --dev package_name`
- **Run with uvicorn directly**: `uv run uvicorn main:app --reload`

## API Documentation

When the server is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON schema**: `http://localhost:8000/openapi.json`

## Production Deployment

For production deployment:

1. Set environment variables as needed
2. Use a production ASGI server like Gunicorn with Uvicorn workers:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
3. Configure reverse proxy (nginx) for static files and SSL
4. Set up monitoring and logging

## Examples

### Quick Start Example

```python
from main import calculate_absolute_humidity

# Calculate absolute humidity
result = calculate_absolute_humidity(25.0, 60)
print(f"Absolute humidity: {result} g/m³")
```

### API Usage Example

```python
import requests

response = requests.post(
    "http://localhost:8000/api/calculate",
    json={"temperature": 25.0, "humidity": 60}
)
data = response.json()
print(f"Absolute humidity: {data['absolute_humidity']} {data['unit']}")
```

## Contributing

1. Install development dependencies: `uv sync --extra dev`
2. Run tests to ensure everything works: `uv run pytest`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `uv run pytest`
6. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute as needed.