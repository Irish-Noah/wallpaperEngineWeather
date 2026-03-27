import requests
import os 
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
LAT = os.getenv('LAT')
LONG = os.getenv('LONG')
APP_PATH = os.getenv('EXE_PATH')
WALLPAPERS = os.getenv('WALLPAPER_PATH')


'''
Function -> categorizes the weather_type to better match the naming convention of the wallpapers
Args -> weather_type: weather type returned from OpenWeatherAPI
Returns -> weather_type: weather type generalized by the function
'''
def generalize_weather_type(weather_type, secondary_description):
    # generalize the weather type
    if weather_type in ['rain', 'drizzle']:
        weather_type = 'rain'
        if weather_type == 'drizzle' and secondary_description in ['heavy', 'shower']:
            weather_type = 'thunderstorm'
    return weather_type

'''
Function -> run CLI command for WallPaperEngine tools to change the wallpaper on monitor 3
Args -> weather_type: new weather type used to determine which wallpaper to set
Returns -> none
'''
def change_wallpaper(weather_type):
    wallpaper_file = WALLPAPERS + fr"\{weather_type}\project.json"
    command = [
        APP_PATH,
        "-control", "openWallpaper",
        "-file", wallpaper_file,
        "-monitor", '2' # indexed starting at 0
    ]
    subprocess.run(command)


'''
Function -> parses the scene.json file on the wallpaper and updates the asset that handles the temperature values
Args -> temp: current temp in F, feels_like: current feels like temp in F, weather_type: current weather to get the correct wallpaper to update
Returns -> none
'''
def update_temps(temp, feels_like, weather_type):
    wallpaper_scene_file = WALLPAPERS + fr"\{weather_type}\scene.json"
    with open(wallpaper_scene_file, "r", encoding="utf-8") as f:
        scene = json.load(f)

    for obj in scene.get("objects", []):
        if obj.get("name") == "TempDisplay":
            obj["text"]["value"] = f"{temp}°F  |  Feels like {feels_like}°F"

    with open(wallpaper_scene_file, "w", encoding="utf-8") as f:
        json.dump(scene, f, indent=2)


'''
Function -> GET request to OpenWeatherAPI to get current weather in my area
Args -> none
Returns -> none
'''
def get_weather(): 
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&units=imperial&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        weather_type = data['weather'][0]['main'].lower()
        secondary_description = data['weather'][0]['description'].lower()
        
        temp = int(data['main'].get('temp'))
        feels_like = int(data['main'].get('feels_like'))
        
        weather_type = generalize_weather_type(weather_type, secondary_description)
        update_temps(temp, feels_like, weather_type)
        change_wallpaper(weather_type) # always change/reload the wallpaper to take temp updates in effect
    else: 
        print(f"Status code {response.status_code} received from API call")


if __name__ == "__main__":
    get_weather()