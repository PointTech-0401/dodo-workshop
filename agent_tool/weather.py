# 天氣 API (60 Calls per minute)
# API doc: https://openweathermap.org/current

import requests
import os

def get_weather(city: str):
    """
    查詢指定城市當前的天氣狀況。
    
    Args:
        city: 英文城市名稱 (例如: Taipei, London, Tokyo)
    """
    api_key = os.getenv("WEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric", # 使用攝氏
    }

    response = requests.get(url, params=params)
    data = response.json()
    #print(f"Received weather data: {data}")

    if response.status_code != 200:
        return f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確(只支援英文城市名稱)。"
    
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    #print(f"Weather description: {weather_desc}, Temperature: {temp}°C, Humidity: {humidity}%")

    return f"天氣概況: {weather_desc}, 溫度: {temp}°C, 濕度: {humidity}%"
