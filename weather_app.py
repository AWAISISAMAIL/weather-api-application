import requests

# API URLs
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# User input
city = input("ENTER CITY NAME: ").strip()

if city == "":
    print("ERROR! PLEASE ENTER CITY NAME")
    exit()


# Finding latitude and longitude
geo_params = {
    "name": city,
    "count": 1,
    "language": "en"
}


try:
    geo_response = requests.get(
        GEO_URL,
        params=geo_params,
        timeout=10
    )

except requests.exceptions.RequestException:
    print("Internet or server connection error!")
    exit()


if geo_response.status_code != 200:
    print("SERVER CONNECTION ERROR")
    exit()


geo_data = geo_response.json()


# Checking city exists
if "results" not in geo_data:
    print(f"Error: City '{city}' not found!")
    exit()


city_info = geo_data["results"][0]

lat = city_info["latitude"]
lon = city_info["longitude"]
country = city_info.get("country", "Unknown")


# Weather API request
weather_params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": True
}


try:
    weather_response = requests.get(
        WEATHER_URL,
        params=weather_params,
        timeout=10
    )

except requests.exceptions.RequestException:
    print("Unable to fetch weather data!")
    exit()


if weather_response.status_code != 200:
    print("Weather API error!")
    exit()


weather_data = weather_response.json()

current = weather_data["current_weather"]


temperature = current["temperature"]
wind_speed = current["windspeed"]
is_day = current.get("is_day", 1)


day_night = "DAY ☀️" if is_day == 1 else "NIGHT 🌙"


# Final Output
print("\n------------------------------------")
print(f"📍 Location: {city.capitalize()}, {country}")
print(f"🌡️ Temperature: {temperature}°C")
print(f"💨 Wind Speed: {wind_speed} km/h")
print(f"🕒 Time: {day_night}")
print("------------------------------------")