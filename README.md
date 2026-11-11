# Assignment11-APIs

In this assignment I started with the OpenSky API to see what planes are over New York. I got each plane’s ID, call sign, position, and whether it was flying, then pulled one plane’s flight path. But I wasn’t sure how it would connect to our custom nodes. So I switched to Poly Haven and Open-Meteo. The idea: get any location’s current weather and time, turn it into a time and sky category, then find a Poly Haven HDRI that matches. Later this could be a custom node that gives image and video gen a real-world lighting reference.

Open-Meteo (real weather) -> time + sky categories -> Poly Haven -> matching HDRI

**Please look at `polyhaven.py` as the main assignment.**

### APIs used: 

- Open Meteo API: https://open-meteo.com/en/docs

- OpenSky Network API: https://openskynetwork.github.io/opensky-api/rest.html#all-state-vectors 

- Poly Haven API: https://redocly.github.io/redoc 

