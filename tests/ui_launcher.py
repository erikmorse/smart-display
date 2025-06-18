"""
UI Launcher for Smart Display tests
Main entry point for running the UI tests
"""
import os
import sys
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.asset_setup import create_mock_assets
from tests.mock_managers import (
    MockWiFiManager, 
    MockLocationManager, 
    MockWeatherManager,
    MockSensorManager,
    MockSpotifyManager,
    MockPhotoManager
)

def setup_environment():
    """Setup environment for testing"""
    print("Setting up test environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""# Smart Display Environment Variables
OPENWEATHERMAP_API_KEY=mock_api_key
GOOGLE_GEOLOCATION_API_KEY=mock_api_key
SPOTIFY_CLIENT_ID=mock_client_id
SPOTIFY_CLIENT_SECRET=mock_client_secret
SPOTIFY_USERNAME=mock_username
SPOTIFY_PASSWORD=mock_password
""")
        print("Created .env file with mock API keys")
    
    # Load environment variables
    load_dotenv()
    
    # Create mock assets
    create_mock_assets()

def monkey_patch_managers():
    """Monkey patch manager classes with mock implementations"""
    print("Patching manager classes with mock implementations...")
    
    # Create utils directory if it doesn't exist
    if not os.path.exists('utils'):
        os.makedirs('utils')
    
    # Create mock manager modules if they don't exist
    manager_modules = [
        'wifi_manager.py',
        'location_manager.py',
        'weather_manager.py',
        'sensor_manager.py',
        'spotify_manager.py',
        'photo_manager.py'
    ]
    
    for module in manager_modules:
        module_path = os.path.join('utils', module)
        if not os.path.exists(module_path):
            create_mock_module(module)
    
    # Import and patch the modules
    from utils.wifi_manager import WiFiManager
    from utils.location_manager import LocationManager
    from utils.weather_manager import WeatherManager
    from utils.sensor_manager import SensorManager
    from utils.spotify_manager import SpotifyManager
    from utils.photo_manager import PhotoManager
    
    # Replace methods with mock implementations
    WiFiManager.scan_networks = MockWiFiManager.scan_networks
    WiFiManager.connect_to_network = MockWiFiManager.connect_to_network
    WiFiManager.is_connected = MockWiFiManager.is_connected
    WiFiManager.save_credentials = MockWiFiManager.save_credentials
    
    LocationManager.get_location = MockLocationManager.get_location
    
    WeatherManager.update_weather = MockWeatherManager.update_weather
    WeatherManager.get_weather_data = MockWeatherManager.get_weather_data
    WeatherManager.get_weather_icon_path = MockWeatherManager.get_weather_icon_path
    
    SensorManager.get_sensor_data = MockSensorManager.get_sensor_data
    
    SpotifyManager.start_monitoring = MockSpotifyManager.start_monitoring
    SpotifyManager.stop_monitoring = MockSpotifyManager.stop_monitoring
    SpotifyManager.get_current_track = MockSpotifyManager.get_current_track
    SpotifyManager.play_pause = MockSpotifyManager.play_pause
    SpotifyManager.next_track = MockSpotifyManager.next_track
    SpotifyManager.previous_track = MockSpotifyManager.previous_track
    
    PhotoManager.start_sync = MockPhotoManager.start_sync
    PhotoManager.stop_sync = MockPhotoManager.stop_sync
    PhotoManager.get_next_photo = MockPhotoManager.get_next_photo
    PhotoManager.get_slideshow_interval = MockPhotoManager.get_slideshow_interval
    PhotoManager.set_slideshow_interval = MockPhotoManager.set_slideshow_interval
    PhotoManager.set_album_id = MockPhotoManager.set_album_id
    
    print("Manager classes patched successfully!")

def create_mock_module(module_name):
    """Create a mock module file"""
    class_name = ''.join(word.capitalize() for word in module_name[:-3].split('_'))
    
    with open(os.path.join('utils', module_name), 'w') as f:
        f.write(f'''"""
Mock {class_name} for Smart Display tests
"""

class {class_name}:
    """Mock {class_name} implementation"""
    
    def __init__(self):
        """Initialize {class_name}"""
        pass
''')
    
    print(f"Created mock module: {module_name}")

def run_app():
    """Run the Smart Display application"""
    print("Starting Smart Display application...")
    
    # Import Kivy modules
    from kivy.config import Config
    
    # Set window size to match Waveshare display (1024x600)
    Config.set('graphics', 'width', '1024')
    Config.set('graphics', 'height', '600')
    
    # Import application
    from main import SmartDisplayApp
    
    # Run application
    try:
        SmartDisplayApp().run()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Setup test environment
    setup_environment()
    
    # Patch manager classes
    monkey_patch_managers()
    
    # Run application
    run_app()
