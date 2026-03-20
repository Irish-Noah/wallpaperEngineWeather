import requests
import os 
import json

url="https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid={API key}"
response = requests.post(url)