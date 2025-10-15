import json
import os
import urllib3

def lambda_handler(event, context):
    city = event.get("queryStringParameters", {}).get("city", "Bangalore")
    api_key = os.environ.get("WEATHER_API_KEY")

    if not api_key:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "API key is missing"})
        }

    http = urllib3.PoolManager()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = http.request('GET', url)

    if response.status != 200:
        return {
            "statusCode": response.status,
            "body": json.dumps({"error": "Failed to fetch weather data"})
        }

    data = json.loads(response.data.decode("utf-8"))

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(weather_info)
    }
