import requests

class WeatherApiHandler:
    def __init__(self, geo_api_key):
        self.geo_api_key = geo_api_key

    def get_geolocation(self, query, config_handler):
        url = f"https://geocode.maps.co/search?q={query}&api_key={self.geo_api_key}"
        response = requests.get(url)
        if response.status_code == 200 and response.json() is not None:
            for item in response.json():
                if config_handler.get_config('defaultCountry') in item.get('display_name'):
                    return item
            raise Exception(f"Location data not found for " + query)
        else:
            raise Exception(f"Failed to fetch location data for " + query)
        
    def get_weather_data(self, lat, lon):
        url = f"https://api.weather.gov/points/{lat},{lon}"
        response = requests.get(url)
        if response.status_code == 200 and response.json() is not None:
            return response.json()
        else:
            print("Raising Exception 2")
            raise Exception("Failed to fetch weather data")
        
    def get_weather_alert_data(self, state):
        url = f"https://api.weather.gov/alerts/active?area={state[0]}"
        response = requests.get(url)
        if response.status_code == 200 and response.json() is not None:
            return response.json()
        else:
            raise Exception("Failed to fetch weather alert data")