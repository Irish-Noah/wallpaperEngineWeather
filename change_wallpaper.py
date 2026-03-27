import requests
import os 
import subprocess
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
LAT = os.getenv('LAT')
LONG = os.getenv('LONG')
APP_PATH = os.getenv('EXE_PATH')
WALLPAPERS = os.getenv('WALLPAPER_PATH')


'''
Function -> parse last_weather.txt to confirm that there has been a change in weather
Args -> weather_type: weather type returned from OpenWeatherAPI
Returns -> boolean: to determine if there has been a change in weather
'''
def check_old_weather(weather_type, secondary_description):
    # generalize the weather type
    if weather_type in ['rain', 'drizzle']:
        weather_type = 'rain'
        if weather_type == 'drizzle' and secondary_description in ['heavy', 'shower']:
            weather_type = 'thunderstorm'
    with open('last_weather.txt', 'r+') as fp:
        if fp.read() != weather_type:
            fp.seek(0)
            fp.write(weather_type)
            fp.truncate()
            fp.close()
            return True
        fp.close()
        return False


'''
Function -> run CLI command for WallPaperEngine tools to change the wallpaper on monitor 3
Args -> weather_type: new weather type used to determine which wallpaper to set
Returns -> none
'''
def change_wallpaper(weather_type):
    exe_path = os.getenv("EXE_PATH")
    wallpapers_path = os.getenv("WALLPAPER_PATH")
    wallpaper_file = wallpapers_path + fr"\{weather_type}\project.json"
    command = [
        exe_path,
        "-control", "openWallpaper",
        "-file", wallpaper_file,
        "-monitor", '2' # indexed starting at 0
    ]
    subprocess.run(command)

'''

'''
def update_temps(temp, feels_like):
    pass


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
        
        update_temps(temp, feels_like, weather_type)

        if check_old_weather(weather_type, secondary_description):
            change_wallpaper(weather_type)
        else:
            print('weather has not changed yet')


if __name__ == "__main__":
    get_weather()