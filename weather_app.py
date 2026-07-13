import requests
# finding lat/long from city name
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
# using lat/long for finding weather forcast
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
city = input("ENTER CITY NAME : ").strip()
if not city:
    print("ERROR! PLEASE ENTER CITY NAME BECAUSE IT IS IMPORTAN")
    exit()
geo_params={"name":city,
            "count":1,
            "language":"en"}
try:
    geo_response = requests.get(
        GEO_URL,
        params=geo_params,
        timeout=10
    )
except requests.exceptions.RequestException:
    print("Internet or server connection error!")
    exit()
geo_response=requests.get(GEO_URL,params=geo_params)
if geo_response.status_code !=200:
    print("SERVER CONNECTION ERROR ")
    exit()
geo_data = geo_response.json()
# cheacking if city was actually found
if "results" not in geo_data:
    print(f"Error: City '{city}' not found. Enter valid city name!")
    exit()
city_info = geo_data["results"][0]
lat = city_info["latitude"]
lon = city_info["longitude"]
country = city_info.get("country","")
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

if weather_response.status_code !=200:
    print("Error: Something wents wrong!")
    exit()

weather_data = weather_response.json()
current = weather_data["current_weather"]
temp = current["temperature"]
wind = current["windspeed"]
is_day = current.get("is_day",1)
#conditon display
day_night = "DAY ☀️" if is_day == 1 else "NIGHT 🌙"
print("\n-----------------------------------------------------")
print(f"📍 Location: {city.capitalize()},{country}")
print(f"🌡️ Temperature: {temp}C")
print(f"💨 Wind Speed: {wind} km/h")
print(f"🕰️ Time Period: {day_night}")
print("-------------------------------------------------------")