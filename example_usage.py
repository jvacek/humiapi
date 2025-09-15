#!/usr/bin/env python3
"""
Example usage script for the Absolute Humidity Calculator Flask app.

This script demonstrates how to:
1. Use the calculation function directly
2. Make HTTP requests to the API
3. Test various scenarios

Run this script with: uv run python example_usage.py
"""

import json
import time
from threading import Thread

import requests

# Import the calculation function directly
from main import calculate_absolute_humidity


def direct_calculation_examples():
    """Examples of using the calculation function directly."""
    print("=" * 60)
    print("DIRECT CALCULATION EXAMPLES")
    print("=" * 60)

    examples = [
        (20.0, 50, "Comfortable room conditions"),
        (25.5, 65, "Warm and humid"),
        (30.0, 80, "Very humid tropical conditions"),
        (0.0, 70, "Cold winter day"),
        (-5.0, 60, "Freezing conditions"),
        (35.0, 90, "Extremely hot and humid"),
        (22.0, 45, "Dry comfortable conditions"),
    ]

    for temp, humidity, description in examples:
        result = calculate_absolute_humidity(temp, humidity)
        print(
            f"{description:.<30} {temp:>6.1f}°C, {humidity:>3d}% RH → {result:>6.2f} g/m³"
        )

    print()


def api_request_examples():
    """Examples of making HTTP requests to the Flask API."""
    print("=" * 60)
    print("API REQUEST EXAMPLES")
    print("=" * 60)

    # Start FastAPI app in a separate thread for demonstration
    def run_app():
        import uvicorn

        uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="error")

    server_thread = Thread(target=run_app, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(3)

    base_url = "http://127.0.0.1:8001"

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"Health check: {response.json()}")
    except Exception as e:
        print(f"Could not connect to server: {e}")
        print(
            "Note: Run 'uv run python main.py' in another terminal to test API requests"
        )
        return

    # Test calculation endpoint
    test_cases = [
        {"temperature": 20.0, "humidity": 50},
        {"temperature": 25.5, "humidity": 65},
        {"temperature": 30.0, "humidity": 80},
        {"temperature": 0.0, "humidity": 30},
    ]

    print("\nAPI Calculations:")
    for i, data in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/api/calculate",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5,
            )

            if response.status_code == 200:
                result = response.json()
                print(
                    f"  {i}. {data['temperature']}°C, {data['humidity']}% → {result['absolute_humidity']} {result['unit']}"
                )
            else:
                print(f"  {i}. Error: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            print(f"  {i}. Request failed: {e}")

    print()


def curl_examples():
    """Show equivalent curl commands for API usage."""
    print("=" * 60)
    print("EQUIVALENT CURL COMMANDS")
    print("=" * 60)

    print("# Health check:")
    print("curl http://localhost:8000/api/health")
    print()

    print("# Calculate absolute humidity:")
    print("curl -X POST http://localhost:8000/api/calculate \\")
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"temperature": 25.5, "humidity": 60}\'')
    print()

    print("# Multiple calculations:")
    examples = [
        {"temperature": 20.0, "humidity": 50},
        {"temperature": 30.0, "humidity": 80},
        {"temperature": 0.0, "humidity": 30},
    ]

    for data in examples:
        print("curl -X POST http://localhost:8000/api/calculate \\")
        print('  -H "Content-Type: application/json" \\')
        print(f"  -d '{json.dumps(data)}'")
        print()


def practical_scenarios():
    """Show practical use case scenarios."""
    print("=" * 60)
    print("PRACTICAL SCENARIOS")
    print("=" * 60)

    scenarios = [
        {
            "name": "Home Comfort Assessment",
            "conditions": [(22.0, 45), (22.0, 55), (22.0, 65)],
            "description": "Compare different humidity levels at room temperature",
        },
        {
            "name": "Greenhouse Monitoring",
            "conditions": [(25.0, 70), (28.0, 70), (25.0, 80)],
            "description": "Optimal growing conditions for plants",
        },
        {
            "name": "Server Room Analysis",
            "conditions": [(18.0, 40), (20.0, 45), (22.0, 50)],
            "description": "Data center environmental conditions",
        },
        {
            "name": "Weather Comparison",
            "conditions": [(35.0, 90), (35.0, 30), (-10.0, 60)],
            "description": "Extreme weather conditions analysis",
        },
    ]

    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print(f"  {scenario['description']}")
        print("  Conditions:")

        for temp, humidity in scenario["conditions"]:
            abs_humidity = calculate_absolute_humidity(temp, humidity)
            print(f"    {temp:>5.1f}°C, {humidity:>2d}% RH → {abs_humidity:>6.2f} g/m³")


def main():
    """Run all examples."""
    print("Absolute Humidity Calculator - Usage Examples")
    print("=" * 60)
    print()

    # Direct calculation examples
    direct_calculation_examples()

    # Practical scenarios
    practical_scenarios()

    # Show curl examples
    curl_examples()

    # Try API examples (might fail if server not running)
    api_request_examples()

    print("=" * 60)
    print("GETTING STARTED")
    print("=" * 60)
    print("1. Start the FastAPI server:")
    print("   uv run python main.py")
    print()
    print("2. Open web interface:")
    print("   http://localhost:8000")
    print()
    print("3. View API documentation:")
    print("   http://localhost:8000/docs (Swagger UI)")
    print("   http://localhost:8000/redoc (ReDoc)")
    print()
    print("4. Use the API programmatically:")
    print("   See the curl examples above")
    print()
    print("5. Import the function directly:")
    print("   from main import calculate_absolute_humidity")
    print("   result = calculate_absolute_humidity(25.0, 60)")


if __name__ == "__main__":
    main()
