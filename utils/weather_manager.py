"""
Weather Manager Module for Smart Display
Handles weather data retrieval and processing
"""
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherManager:
    """Manages weather data retrieval and processing"""
    
    def __init__(self):
        """Initialize Weather Manager"""
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'config', 'weather.json')
        self.weather_data = self.load_saved_weather()
        self.last_update = None
    
    def load_saved_weather(self):
        """Load saved weather data from config file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading saved weather: {e}")
                return None
        return None
    
    def save_weather(self, weather_data):
        """Save weather data to config file"""
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(weather_data, f)
        
        self.weather_data = weather_data
        self.last_update = datetime.now()
    
    def update_weather(self, location):
        """Update weather data using OpenWeatherMap API"""
        # If we don't have an API key, fail
        if not self.api_key:
            print("No OpenWeatherMap API key found. Set OPENWEATHERMAP_API_KEY in .env file.")
            return False
        
        try:
            # Check if we need to update (less than 30 minutes since last update)
            if self.last_update:
                time_since_update = (datetime.now() - self.last_update).total_seconds() / 60
                if time_since_update < 30 and self.weather_data:
                    return True
            
            # Get current weather
            current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lng']}&appid={self.api_key}&units=metric"
            current_response = requests.get(current_url)
            
            # Get forecast
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={location['lat']}&lon={location['lng']}&appid={self.api_key}&units=metric"
            forecast_response = requests.get(forecast_url)
            
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                current_data = current_response.json()
                forecast_data = forecast_response.json()
                
                # Process the data
                weather_data = self._process_weather_data(current_data, forecast_data)
                
                # Save the weather data
                self.save_weather(weather_data)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating weather: {e}")
            return False
    
    def _process_weather_data(self, current_data, forecast_data):
        """Process weather data from API responses"""
        # Process current weather
        current = {
            'temp': current_data['main']['temp'],
            'feels_like': current_data['main']['feels_like'],
            'humidity': current_data['main']['humidity'],
            'pressure': current_data['main']['pressure'],
            'wind_speed': current_data['wind']['speed'],
            'wind_direction': current_data['wind']['deg'],
            'description': current_data['weather'][0]['description'],
            'icon': current_data['weather'][0]['icon'],
            'city': current_data['name'],
            'country': current_data['sys']['country'],
            'sunrise': current_data['sys']['sunrise'],
            'sunset': current_data['sys']['sunset'],
            'timestamp': current_data['dt']
        }
        
        # Process forecast
        forecast = []
        
        # Group forecasts by day
        days = {}
        
        for item in forecast_data['list']:
            # Convert timestamp to date
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            
            if date not in days:
                days[date] = []
            
            days[date].append({
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind']['deg'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'timestamp': item['dt'],
                'time': datetime.fromtimestamp(item['dt']).strftime('%H:%M')
            })
        
        # Process each day
        for date, items in days.items():
            # Get min and max temperatures
            temps = [item['temp'] for item in items]
            min_temp = min(temps)
            max_temp = max(temps)
            
            # Get most common icon
            icons = [item['icon'] for item in items]
            icon = max(set(icons), key=icons.count)
            
            # Get most common description
            descriptions = [item['description'] for item in items]
            description = max(set(descriptions), key=descriptions.count)
            
            # Add to forecast
            forecast.append({
                'date': date,
                'min_temp': min_temp,
                'max_temp': max_temp,
                'icon': icon,
                'description': description,
                'hourly': items
            })
        
        # Sort forecast by date
        forecast.sort(key=lambda x: x['date'])
        
        # Limit to 5 days
        forecast = forecast[:5]
        
        return {
            'current': current,
            'forecast': forecast,
            'last_update': datetime.now().isoformat()
        }
    
    def get_weather_data(self):
        """Get the current weather data"""
        return self.weather_data
    
    def get_weather_icon_path(self, icon_code):
        """Get the path to a weather icon"""
        # Map OpenWeatherMap icon codes to local icon files
        icon_map = {
            '01d': 'clear_day.png',
            '01n': 'clear_night.png',
            '02d': 'partly_cloudy_day.png',
            '02n': 'partly_cloudy_night.png',
            '03d': 'cloudy.png',
            '03n': 'cloudy.png',
            '04d': 'cloudy.png',
            '04n': 'cloudy.png',
            '09d': 'rain.png',
            '09n': 'rain.png',
            '10d': 'rain_day.png',
            '10n': 'rain_night.png',
            '11d': 'thunderstorm.png',
            '11n': 'thunderstorm.png',
            '13d': 'snow.png',
            '13n': 'snow.png',
            '50d': 'fog.png',
            '50n': 'fog.png'
        }
        
        # Get the icon filename
        icon_file = icon_map.get(icon_code, 'unknown.png')
        
        # Return the path
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'assets', 'weather_icons', icon_file)
