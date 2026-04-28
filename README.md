### Project Overview

I didn't like how the Microsoft Taskbar Weather Widget would switch to the news or stocks whenever it wanted to. The temperatures were always a little off too, so I decided to spice up my desktop a little bit. 

I used Wallpaper Engine from Steam to accomplish this. I created a few variants of the same wallpaper to reflect the weather (i.e. sun rays in the sun, harsh winds and heavy rain for thunderstorms, etc.). Then I used [OpenWeather's API](https://openweathermap.org/api/one-call-3?collection=one_call_api_3.0) to get the weather in my current location. I put the returned API response into a custom Wallpaper Engine JSON object and placed that in each of my weather variant wallpapers config files. Then I used Microsoft's Task Scheduler app to create, essentially, a cron job that runs every 15 minutes to update the wallpaper based on the weather!

### Weather Report

<details>
  <summary>Open for Weather Report</summary>
  <img src="images\weatherReport.png" alt='weather report' width="500" height="500"/>
</details>
