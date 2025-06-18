#!/usr/bin/env python3
"""
Test script to run the Smart Display application with mock data
"""
import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create mock assets
def create_mock_assets():
    """Create mock assets for testing"""
    # Create directories if they don't exist
    os.makedirs('assets/weather_icons', exist_ok=True)
    os.makedirs('assets/photos', exist_ok=True)
    os.makedirs('config', exist_ok=True)
    
    # Create mock weather icons (simple colored rectangles)
    from PIL import Image, ImageDraw
    
    # Weather icon codes from OpenWeatherMap
    icon_codes = [
        '01d', '01n',  # clear sky
        '02d', '02n',  # few clouds
        '03d', '03n',  # scattered clouds
        '04d', '04n',  # broken clouds
        '09d', '09n',  # shower rain
        '10d', '10n',  # rain
        '11d', '11n',  # thunderstorm
        '13d', '13n',  # snow
        '50d', '50n',  # mist
    ]
    
    # Colors for each icon type
    icon_colors = {
        '01': (255, 255, 0),    # yellow (sun)
        '02': (200, 200, 255),  # light blue (few clouds)
        '03': (150, 150, 200),  # blue-gray (scattered clouds)
        '04': (100, 100, 150),  # darker blue-gray (broken clouds)
        '09': (100, 100, 255),  # blue (shower rain)
        '10': (0, 0, 255),      # darker blue (rain)
        '11': (128, 0, 128),    # purple (thunderstorm)
        '13': (255, 255, 255),  # white (snow)
        '50': (200, 200, 200),  # gray (mist)
    }
    
    # Create each icon
    for code in icon_codes:
        img = Image.new('RGB', (100, 100), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        
        # Get color based on the first two characters of the code
        color = icon_colors.get(code[:2], (255, 0, 0))
        
        # Draw a colored rectangle
        draw.rectangle([(10, 10), (90, 90)], fill=color)
        
        # Save the image
        img.save(f'assets/weather_icons/{code}.png')
    
    # Create mock album art for Spotify
    album_img = Image.new('RGB', (300, 300), color=(20, 20, 20))
    draw = ImageDraw.Draw(album_img)
    draw.ellipse([(50, 50), (250, 250)], fill=(30, 215, 96))  # Spotify green
    album_img.save('assets/album_art.png')
    
    # Create mock photos for slideshow
    for i in range(5):
        photo = Image.new('RGB', (800, 600), color=(0, 0, 0))
        draw = ImageDraw.Draw(photo)
        
        # Draw different colored rectangles for each photo
        colors = [
            (255, 0, 0),    # red
            (0, 255, 0),    # green
            (0, 0, 255),    # blue
            (255, 255, 0),  # yellow
            (0, 255, 255),  # cyan
        ]
        
        draw.rectangle([(100, 100), (700, 500)], fill=colors[i])
        draw.text((400, 300), f"Photo {i+1}", fill=(255, 255, 255))
        
        photo.save(f'assets/photos/photo{i+1}.jpg')
    
    # Create empty config files
    with open('config/wifi.json', 'w') as f:
        f.write('{"saved_networks": []}')
    
    with open('config/location.json', 'w') as f:
        f.write('{"city": "New York", "country": "US", "lat": 40.7128, "lon": -74.0060}')
    
    with open('config/weather.json', 'w') as f:
        f.write('{"last_update": "2025-06-17T12:00:00"}')
    
    with open('config/spotify.json', 'w') as f:
        f.write('{"refresh_token": "mock_refresh_token"}')
    
    print("Mock assets created successfully!")

# Monkey patch the manager classes to use mock data
def monkey_patch_managers():
    """Monkey patch manager classes to use mock data"""
    # Use mock WiFi manager for Windows
    import sys
    import os
    
    # Create utils directory if it doesn't exist
    os.makedirs('utils', exist_ok=True)
    
    # Create __init__.py in utils directory if it doesn't exist
    if not os.path.exists('utils/__init__.py'):
        with open('utils/__init__.py', 'w') as f:
            f.write('"""Utils package for Smart Display"""')
    
    # Create mock manager modules if they don't exist
    required_modules = [
        'location_manager.py',
        'weather_manager.py',
        'sensor_manager.py',
        'spotify_manager.py',
        'photo_manager.py'
    ]
    
    for module in required_modules:
        module_path = os.path.join('utils', module)
        if not os.path.exists(module_path):
            with open(module_path, 'w') as f:
                class_name = ''.join(word.capitalize() for word in module.split('_'))
                class_name = class_name.replace('.py', '')
                
                # Create module content
                content = f"""\"\"\"
{class_name} for Smart Display
\"\"\"

class {class_name}:
    \"\"\"
    Mock {class_name} class
    \"\"\"
    
    def __init__(self):
        \"\"\"
        Initialize {class_name}
        \"\"\"
        pass
"""
                f.write(content)
    
    # Use our mock WiFi manager
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Create mock WiFi manager if it doesn't exist
    if not os.path.exists('utils/wifi_manager.py'):
        # Copy the mock WiFi manager to the real location
        if os.path.exists('utils/wifi_manager_mock.py'):
            with open('utils/wifi_manager_mock.py', 'r') as src:
                with open('utils/wifi_manager.py', 'w') as dst:
                    dst.write(src.read())
        else:
            # Create a basic mock if the mock file doesn't exist
            with open('utils/wifi_manager.py', 'w') as f:
                f.write("""\"\"\"WiFi Manager for Smart Display\"\"\"

class WiFiManager:
    \"\"\"Mock WiFi Manager class\"\"\"
    
    def __init__(self):
        \"\"\"Initialize WiFi Manager\"\"\"
        self.is_connected_state = True
    
    def scan_networks(self):
        \"\"\"Scan for available WiFi networks\"\"\"
        return [
            {"ssid": "Home WiFi", "signal": 90, "security": "WPA2"},
            {"ssid": "Neighbor's WiFi", "signal": 70, "security": "WPA2"},
            {"ssid": "Coffee Shop", "signal": 50, "security": "Open"},
        ]
    
    def connect_to_network(self, ssid, password=None):
        \"\"\"Connect to a WiFi network\"\"\"
        return True
    
    def is_connected(self):
        \"\"\"Check if connected to a network\"\"\"
        return self.is_connected_state
""")
    
    # Now import the modules
    from utils.wifi_manager import WiFiManager
    from utils.location_manager import LocationManager
    from utils.weather_manager import WeatherManager
    from utils.sensor_manager import SensorManager
    from utils.spotify_manager import SpotifyManager
    from utils.photo_manager import PhotoManager
    
    # Patch WiFiManager
    original_scan = WiFiManager.scan_networks
    def mock_scan_networks(self):
        return [
            {"ssid": "Home WiFi", "signal": 90, "security": "WPA2"},
            {"ssid": "Neighbor's WiFi", "signal": 70, "security": "WPA2"},
            {"ssid": "Coffee Shop", "signal": 50, "security": "Open"},
            {"ssid": "Guest Network", "signal": 30, "security": "WEP"},
        ]
    WiFiManager.scan_networks = mock_scan_networks
    
    original_connect = WiFiManager.connect_to_network
    def mock_connect(self, ssid, password=None):
        print(f"Mock connecting to {ssid} with password {password}")
        return True
    WiFiManager.connect_to_network = mock_connect
    
    original_is_connected = WiFiManager.is_connected
    def mock_is_connected(self):
        return True  # Always return connected for testing
    WiFiManager.is_connected = mock_is_connected
    
    # Patch LocationManager
    original_get_location = LocationManager.get_location
    def mock_get_location(self, success_callback, failure_callback):
        location = {
            "city": "New York",
            "country": "US",
            "lat": 40.7128,
            "lon": -74.0060
        }
        success_callback(location)
    LocationManager.get_location = mock_get_location
    
    # Patch WeatherManager
    original_update_weather = WeatherManager.update_weather
    def mock_update_weather(self, location):
        self.weather_data = {
            "current": {
                "city": location["city"],
                "country": location["country"],
                "temp": 22,
                "feels_like": 23,
                "description": "clear sky",
                "icon": "01d",
                "humidity": 65,
                "pressure": 1013,
                "wind_speed": 5.2,
                "wind_direction": "NE",
                "sunrise": "06:24",
                "sunset": "20:30"
            },
            "forecast": [
                {
                    "date": "2025-06-18",
                    "min_temp": 18,
                    "max_temp": 24,
                    "description": "few clouds",
                    "icon": "02d"
                },
                {
                    "date": "2025-06-19",
                    "min_temp": 19,
                    "max_temp": 26,
                    "description": "scattered clouds",
                    "icon": "03d"
                },
                {
                    "date": "2025-06-20",
                    "min_temp": 20,
                    "max_temp": 28,
                    "description": "rain",
                    "icon": "10d"
                },
                {
                    "date": "2025-06-21",
                    "min_temp": 19,
                    "max_temp": 25,
                    "description": "thunderstorm",
                    "icon": "11d"
                },
                {
                    "date": "2025-06-22",
                    "min_temp": 17,
                    "max_temp": 23,
                    "description": "clear sky",
                    "icon": "01d"
                }
            ]
        }
        return True
    WeatherManager.update_weather = mock_update_weather
    
    original_get_icon = WeatherManager.get_weather_icon_path
    def mock_get_icon(self, icon_code):
        return f"assets/weather_icons/{icon_code}.png"
    WeatherManager.get_weather_icon_path = mock_get_icon
    
    # Patch SensorManager
    original_get_sensor = SensorManager.get_sensor_data
    def mock_get_sensor(self):
        return {
            "temperature": 21.5,
            "humidity": 55,
            "pressure": 1010,
            "gas": 12000,
            "air_quality": 85
        }
    SensorManager.get_sensor_data = mock_get_sensor
    
    # Patch SpotifyManager
    original_get_current = SpotifyManager.get_current_track
    def mock_get_current(self):
        return {
            "name": "Mock Song Title",
            "artist": "Mock Artist",
            "album": "Mock Album",
            "album_art_path": "assets/album_art.png",
            "duration_ms": 180000,
            "progress_ms": 45000,
            "is_playing": True
        }
    SpotifyManager.get_current_track = mock_get_current
    
    original_play_pause = SpotifyManager.play_pause
    def mock_play_pause(self):
        print("Mock play/pause toggled")
        return True
    SpotifyManager.play_pause = mock_play_pause
    
    original_next = SpotifyManager.next_track
    def mock_next(self):
        print("Mock next track")
        return True
    SpotifyManager.next_track = mock_next
    
    original_prev = SpotifyManager.previous_track
    def mock_prev(self):
        print("Mock previous track")
        return True
    SpotifyManager.previous_track = mock_prev
    
    # Patch PhotoManager
    original_get_next = PhotoManager.get_next_photo
    def mock_get_next(self):
        import random
        return f"assets/photos/photo{random.randint(1, 5)}.jpg"
    PhotoManager.get_next_photo = mock_get_next
    
    original_get_interval = PhotoManager.get_slideshow_interval
    def mock_get_interval(self):
        return 5  # 5 seconds for testing
    PhotoManager.get_slideshow_interval = mock_get_interval
    
    print("Managers patched with mock data!")

if __name__ == "__main__":
    try:
        # Check if PIL is installed
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("Pillow is required for creating mock assets.")
            print("Please install it with: pip install Pillow")
            sys.exit(1)
        
        # Create mock assets
        create_mock_assets()
        
        # Monkey patch managers
        monkey_patch_managers()
        
        print("Starting Smart Display application with mock data...")
        print("Press Ctrl+C to exit")
        
        # Import and run the application
        from main import SmartDisplayApp
        SmartDisplayApp().run()
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
