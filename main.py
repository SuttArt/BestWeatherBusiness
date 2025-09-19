import requests
from dotenv import load_dotenv
import os
import json

def get_coordinates():
    api_key = os.getenv("API_KEY")
    params = [
        {
            "q": "Berlin, DE",
            "appid": api_key
        },
        {
            "q": "Kyiv, UA",
            "appid": api_key
        }
    ]

    # Get Coordinates by location name
    # More info under: https://openweathermap.org/api/geocoding-api
    # List of ISO 3166 country codes: https://www.iso.org/obp/ui/
    url = 'http://api.openweathermap.org/geo/1.0/direct'

    # return value
    location_data = []

    for city in params:
        try:
            # Make a GET request to the API endpoint using requests.get()
            response = requests.get(url, params=city)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                response_data = response.json()
                if response_data:
                    location_data.append({
                        "name": response_data[0]["name"],
                        "lat": response_data[0]["lat"],
                        "lon": response_data[0]["lon"],
                        "country": response_data[0]["country"],
                    }
                    )
            else:
                print('Error:', response.status_code)

        except requests.exceptions.RequestException as e:
            # Handle any network-related errors or exceptions
            print('Error:', e)

    return location_data


def get_weather(location_data):
    api_key = os.getenv("API_KEY")
    params = {
        "lat": location_data["lat"],
        "lon": location_data["lon"],
        "appid": api_key
    }

    url = 'https://api.openweathermap.org/data/2.5/weather'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            print('Error Code:', response.status_code)
            print('Error Text:', response.text)
            return None

    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


def main():
    load_dotenv()

    # get latitude and longitude
    # We can actually hardcoded it, do not neet to call it every time
    coordinates_data = get_coordinates()

    if coordinates_data:
        # collect everything here
        all_data = []
        print("Coordinates:", coordinates_data)

        for city in coordinates_data:
            weather_data = get_weather(city)
            if weather_data:
                print("Weather:", weather_data)
                all_data.append({
                    "city": city,
                    "weather": weather_data
                })
            else:
                print('Failed to fetch weather data for', city["name"])

            # Write collected data to JSON file
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)

            print("Data written to data.json")
    else:
        print('Failed to fetch coordinates data from coordinates API.')


if __name__ == '__main__':
    main()
