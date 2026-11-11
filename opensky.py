import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
from datetime import datetime

# states/all mean "current plane positions"
url = "https://opensky-network.org/api/states/all"

# a box on the map around New York.
my_params = {
    'lamin': 40.4,    # south edge (min latitude)
    'lomin': -74.4,   # west edge (min longitude)
    'lamax': 41.0,    # north edge (max latitude)
    'lomax': -73.5    # east edge (max longitude)
}

# 1. “What planes are over New York right now?
response = requests.get(url, params=my_params) # add the box to the URL and store in response
data = response.json() # turn the reply into Python dictionary
print(data)

# take data and save it as a proper json file
with open("planes.json", "w") as f:
    json.dump(data, f, indent=2) 

# the dictionary has two keys: 'time' and 'states'
planes = data['states'] or [] # the list of planes is in the 'states' key
snapshot = datetime.fromtimestamp(data['time']) # fomrat the timestamp into a datetime object
formatted_time = snapshot.strftime("%Y-%m-%d %I:%M %p")

print(f"Found {len(planes)} planes at {formatted_time}")

plane = next(p for p in planes if p[6] is not None and p[8] == False)   # one folder: first plane with a location
print("picked:", plane[0], plane[1])





track_url = "https://opensky-network.org/api/tracks/all"
track_params = {
    'icao24': plane[0].lower(),
    'time': 0          # 0 = live track
}

r = requests.get(track_url, params=track_params, timeout=30)
print("track status:", r.status_code)

if r.status_code == 200:
    track = r.json()
    print("callsign:", track['callsign'])
    print("points:", len(track['path']))
    for point in track['path'][:5]:     # first 5 points
        print(point)