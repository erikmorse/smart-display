"""
Mock managers module for Smart Display tests
Provides mock implementations of all manager classes
"""
import os
import time
import json
from datetime import datetime, timedelta

class MockWiFiManager:
    """Mock WiFi Manager class"""
    
    def __init__(self):
        """Initialize WiFi Manager"""
        self.is_connected_state = True
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        return [
            {
                'ssid': 'Home Network',
                'signal': 90,
                'security': 'WPA2'
            },
            {
                'ssid': 'Neighbor WiFi',
                'signal': 60,
                'security': 'WPA2'
            },
            {
                'ssid': 'Guest Network',
                'signal': 80,
                'security': 'Open'
            },
            {
                'ssid': 'Office WiFi',
                'signal': 30,
                'security': 'WPA2-Enterprise'
            }
        ]
    
    def connect_to_network(self, ssid, password=None):
        """Connect to a WiFi network"""
        print(f"Mock connecting to network: {ssid}")
        return True
    
    def is_connected(self):
        """Check if connected to WiFi"""
        return self.is_connected_state
    
    def save_credentials(self, ssid, password):
        """Save WiFi credentials to .env file"""
        # In the mock, we'll just print and update .env
        print(f"Mock saving credentials for: {ssid}")
        
        env_path = '.env'
        env_vars = {}
        
        # Read existing .env file
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, val = line.strip().split('=', 1)
                        env_vars[key] = val
        
        # Update WiFi credentials
        env_vars['WIFI_SSID'] = ssid
        if password:
            env_vars['WIFI_PASSWORD'] = password
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            for key, val in env_vars.items():
                f.write(f"{key}={val}\n")
        
        return True


class MockLocationManager:
    """Mock Location Manager class"""
    
    def __init__(self):
        """Initialize Location Manager"""
        pass
    
    def get_location(self, success_callback, failure_callback):
        """Get location using Google Geolocation API"""
        # Mock successful location retrieval
        location = {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'city': 'New York',
            'country': 'US'
        }
        
        # Call success callback with mock location
        if success_callback:
            success_callback(location)
        
        return location


class MockWeatherManager:
    """Mock Weather Manager class"""
    
    def __init__(self):
        """Initialize Weather Manager"""
        self.weather_data = None
    
    def update_weather(self, location):
        """Update weather data for location"""
        # Mock weather data
        current_temp = 72  # Fahrenheit
        current_time = datetime.now()
        
        self.weather_data = {
            'current': {
                'temp': current_temp,
                'feels_like': current_temp - 2,
                'humidity': 65,
                'pressure': 1015,
                'wind_speed': 5.2,
                'weather': [
                    {
                        'id': 800,
                        'main': 'Clear',
                        'description': 'clear sky',
                        'icon': '01d'
                    }
                ],
                'dt': int(current_time.timestamp())
            },
            'hourly': [
                {
                    'dt': int((current_time + timedelta(hours=i)).timestamp()),
                    'temp': current_temp + i,
                    'weather': [{'icon': f'0{(i % 5) + 1}d'}]
                }
                for i in range(24)
            ],
            'daily': [
                {
                    'dt': int((current_time + timedelta(days=i)).timestamp()),
                    'temp': {
                        'min': current_temp - 5 + i,
                        'max': current_temp + 5 + i
                    },
                    'weather': [{'icon': f'0{(i % 5) + 1}d'}]
                }
                for i in range(7)
            ],
            'location': {
                'city': location.get('city', 'New York'),
                'country': location.get('country', 'US')
            }
        }
        
        return self.weather_data
    
    def get_weather_data(self):
        """Get current weather data"""
        if not self.weather_data:
            self.update_weather({'city': 'New York', 'country': 'US'})
        
        return self.weather_data
    
    def get_weather_icon_path(self, icon_code):
        """Get path to weather icon"""
        return f'assets/weather_icons/{icon_code}.png'


class MockSensorManager:
    """Mock Sensor Manager class"""
    
    def __init__(self):
        """Initialize Sensor Manager"""
        pass
    
    def get_sensor_data(self):
        """Get sensor data from BME680"""
        # Mock sensor data
        return {
            'temperature': 22.5,  # Celsius
            'humidity': 45.2,
            'pressure': 1013.25,
            'gas': 12500
        }


class MockSpotifyManager:
    """Mock Spotify Manager class"""
    
    def __init__(self, status_callback=None):
        """Initialize Spotify Manager"""
        self.is_playing = False
        self.current_track = None
        self.status_callback = status_callback
    
    def start_monitoring(self):
        """Start monitoring Spotify status"""
        # Mock initial track
        self.current_track = {
            'name': 'Mock Song Title',
            'artist': 'Mock Artist',
            'album': 'Mock Album',
            'album_art': 'assets/icons/album.jpg',
            'duration': 180,  # seconds
            'position': 45    # seconds
        }
        
        # Call status callback if provided
        if self.status_callback:
            self.status_callback(False, self.current_track)
    
    def stop_monitoring(self):
        """Stop monitoring Spotify status"""
        pass
    
    def get_current_track(self):
        """Get current track information"""
        return self.current_track
    
    def play_pause(self):
        """Toggle play/pause"""
        self.is_playing = not self.is_playing
        
        # Call status callback if provided
        if self.status_callback:
            self.status_callback(self.is_playing, self.current_track)
        
        return self.is_playing
    
    def next_track(self):
        """Skip to next track"""
        # Mock next track
        self.current_track = {
            'name': 'Next Mock Song',
            'artist': 'Mock Artist',
            'album': 'Mock Album',
            'album_art': 'assets/icons/album.jpg',
            'duration': 210,  # seconds
            'position': 0     # seconds
        }
        
        # Call status callback if provided
        if self.status_callback:
            self.status_callback(self.is_playing, self.current_track)
    
    def previous_track(self):
        """Go back to previous track"""
        # Mock previous track
        self.current_track = {
            'name': 'Previous Mock Song',
            'artist': 'Mock Artist',
            'album': 'Mock Album',
            'album_art': 'assets/icons/album.jpg',
            'duration': 160,  # seconds
            'position': 0     # seconds
        }
        
        # Call status callback if provided
        if self.status_callback:
            self.status_callback(self.is_playing, self.current_track)


class MockPhotoManager:
    """Mock Photo Manager class"""
    
    def __init__(self):
        """Initialize Photo Manager"""
        self.photos = [f'assets/photos/photo_{i}.jpg' for i in range(5)]
        self.current_index = 0
        self.config = {
            'album_id': 'mock_album_id',
            'slideshow_interval': 30
        }
    
    def start_sync(self):
        """Start syncing photos"""
        pass
    
    def stop_sync(self):
        """Stop syncing photos"""
        pass
    
    def get_next_photo(self):
        """Get next photo for slideshow"""
        photo = self.photos[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.photos)
        return photo
    
    def get_slideshow_interval(self):
        """Get slideshow interval in seconds"""
        return self.config.get('slideshow_interval', 30)
    
    def set_slideshow_interval(self, interval):
        """Set slideshow interval in seconds"""
        self.config['slideshow_interval'] = interval
    
    def set_album_id(self, album_id):
        """Set Google Photos album ID"""
        self.config['album_id'] = album_id
