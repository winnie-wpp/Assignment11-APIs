import requests
from datetime import datetime
import random 
import json

# API: https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m

# 1. “What is the weather in New York right now?” with Open-Meteo API
url = "https://api.open-meteo.com/v1/forecast"
my_params = {
    'latitude': 40.71,
    'longitude': -74.01,
    'current': 'cloud_cover,is_day,weather_code,visibility',
    'daily': 'sunrise,sunset',
    'timezone': 'auto',
    'forecast_days': 1
}

meteo_response = requests.get(url, params=my_params)
weather = meteo_response.json()

print(weather['current'])
print(weather['daily'])

# 2. Turn the times into datetime objects
# get sunrise, sunset, and noon times
current = weather['current']
weather_code = current['weather_code']

now = datetime.fromisoformat(current['time'])
sunrise = datetime.fromisoformat(weather['daily']['sunrise'][0])
sunset = datetime.fromisoformat(weather['daily']['sunset'][0])
noon = sunrise + (sunset - sunrise) / 2

# 3. Categorize the time of day
if current['is_day'] == 0:
    time_category = 'night'
elif abs((now - sunrise).total_seconds()) < 3600 or abs((now - sunset).total_seconds()) < 3600:
    time_category = 'sunrise-sunset'
elif abs((now - noon).total_seconds()) < 7200:
    time_category = 'midday'
else:
    time_category = 'morning-afternoon'

# 4. Categorize the sky conditions based on cloud cover
if current['cloud_cover'] < 20:
    sky_category = 'clear'
elif current['cloud_cover'] < 70:
    sky_category = 'partly cloudy'
else:
    sky_category = 'overcast'

# Categorize the sky conditions based on weather code
# if current['weather_code'] in [0]:
#     sky_category = 'clear'
# elif current['weather_code'] in [1, 2]:
#     sky_category = 'mainly clear'
# elif current['weather_code'] in [3]:
#     sky_category = 'overcast'

print("time:", time_category)
print("sky:", sky_category)


# 5. Use the Polyhaven API to find HDRIs that match the time of day and sky conditions
headers = {
    "User-Agent": "my-class-assinment"
    }

ph_url = "https://api.polyhaven.com/assets"

# t = type (hdris, textures, models), c = category
ph_params = {
    't': 'hdris', 
    'c': time_category
}

ph_response = requests.get(ph_url, headers=headers, params=ph_params)
hdris = ph_response.json()

# first_id = list(hdris)[0]
# print(json.dumps(hdris[first_id], indent=2))

# 6. Filter the HDRIs by sky category
matches = [] # create empty list

# goses thru all the HDRIs and checks if the sky category is in the categories of the HDRI
for hdri_id in hdris:
    if sky_category in hdris[hdri_id]['categories']:
        matches.append(hdri_id) # add the matching HDRI to the list

# show how many were found and how many matched the sky category
print(f"{len(hdris)} {time_category} HDRIs, {len(matches)} also {sky_category}")

# 7. Pick a random HDRI from the matches, or from all HDRIs if no matches
if matches:
    pick = random.choice(matches)
    print(f"Found a match for {time_category} + {sky_category}.")
else:
    pick = random.choice(list(hdris))
    print(f"No {sky_category} HDRIs for {time_category}, here's a random {time_category} HDRI instead.")

# final output of the HDRI pick
print("\nHDRI pick:")
print("HDRI:", hdris[pick]['name'])
print("tags:", hdris[pick]['tags'])
print("page:", f"https://polyhaven.com/a/{pick}")