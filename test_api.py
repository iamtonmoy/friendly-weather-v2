import requests
from datetime import datetime
from dotenv import load_dotenv
import os 

load_dotenv()

def get_season(month):
    if 3 <= month <= 5:
        return "Spring"
    elif 6 <= month <= 8:
        return "Summer"
    elif 9 <= month <= 11:
        return "Autumn"
    else:
        return "Winter"

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Check if the API request was successful
        if response.status_code == 200:
            # Extracting relevant weather information
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            wind_direction = data['wind']['deg']
            city_name = data['name']
            pressure = data['main']['pressure']
            visibility = data.get('visibility', 'N/A')

            # Extracting cloudiness information
            cloudiness = data['clouds']['all'] if 'clouds' in data else 'N/A'

            # Extracting date information
            timestamp = data['dt']
            date = datetime.utcfromtimestamp(timestamp)
            month = date.month
            season = get_season(month)

            # Display the extracted information
            print(f"Weather information for {city_name} ({season}):")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Wind Direction: {wind_direction}°")
            print(f"Pressure: {pressure} hPa")
            print(f"Visibility: {visibility} meters")
            print(f"Cloudiness: {cloudiness}%")

        elif response.status_code == 401:
            print("Error: Invalid API key. Please check your API key.")
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = os.getenv("fk_api_key")
    city_name = input("Enter the city name: ")

    get_weather(api_key, city_name)