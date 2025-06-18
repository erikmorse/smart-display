#!/usr/bin/env python3
"""
Smart Display Application for Raspberry Pi Zero 2W
"""
import os
import sys
import time
import threading
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Kivy modules
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.logger import Logger

# Import application modules
from app.screens.weather_screen import WeatherScreen
from app.screens.wifi_screen import WiFiScreen
from app.screens.spotify_screen import SpotifyScreen
from app.screens.screensaver_screen import ScreensaverScreen
from app.screens.settings_screen import SettingsScreen

from utils.wifi_manager import WiFiManager
from utils.location_manager import LocationManager
from utils.weather_manager import WeatherManager
from utils.sensor_manager import SensorManager
from utils.spotify_manager import SpotifyManager
from utils.photo_manager import PhotoManager

# Set default window touch time
Window.last_touch_time = time.time()

class SmartDisplayApp(App):
    """Main application class for the Smart Display"""
    
    # Managers
    wifi_manager = ObjectProperty(None)
    location_manager = ObjectProperty(None)
    weather_manager = ObjectProperty(None)
    sensor_manager = ObjectProperty(None)
    spotify_manager = ObjectProperty(None)
    photo_manager = ObjectProperty(None)
    
    # App state
    current_screen = StringProperty('weather')
    screensaver_timeout = NumericProperty(300)  # 5 minutes default
    is_spotify_playing = BooleanProperty(False)
    weather_update_interval = NumericProperty(1800)  # 30 minutes default
    
    def build(self):
        """Build the application"""
        # Set window size to match display (1024x600)
        Window.size = (1024, 600)
        
        # Initialize managers
        self.wifi_manager = WiFiManager()
        self.location_manager = LocationManager()
        self.weather_manager = WeatherManager()
        self.sensor_manager = SensorManager()
        self.photo_manager = PhotoManager()
        
        # Initialize Spotify manager with a delay to prevent premature callbacks
        self.spotify_manager = None
        
        # Create root layout with navigation
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.graphics import Color, Rectangle
        
        root = BoxLayout(orientation='vertical')
        
        # Create screen manager with custom transition
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Add all screens normally
        self.sm.add_widget(WeatherScreen(name='weather'))
        self.sm.add_widget(WiFiScreen(name='wifi'))
        self.sm.add_widget(SpotifyScreen(name='spotify'))
        self.sm.add_widget(ScreensaverScreen(name='screensaver'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        
        # Add screen manager to root layout (takes most of the space)
        root.add_widget(self.sm)
        
        # Create navigation bar
        nav_bar = BoxLayout(size_hint=(1, 0.08), spacing=10, padding=[5, 5])
        
        # Add background color using canvas instructions
        with nav_bar.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.nav_bg = Rectangle(pos=nav_bar.pos, size=nav_bar.size)
            
        # Update rectangle position and size when the layout changes
        def update_rect(instance, value):
            self.nav_bg.pos = instance.pos
            self.nav_bg.size = instance.size
            
        nav_bar.bind(pos=update_rect, size=update_rect)
        
        # Store navigation buttons as instance variables to access them later
        self.nav_buttons = {}
        
        # Add navigation buttons
        self.nav_buttons['weather'] = Button(text='Weather', background_color=(0.2, 0.6, 1, 1))
        self.nav_buttons['screensaver'] = Button(text='Photos', background_color=(0.8, 0.4, 0.2, 1))
        self.nav_buttons['spotify'] = Button(text='Spotify', background_color=(0.1, 0.7, 0.3, 1))
        self.nav_buttons['settings'] = Button(text='Settings', background_color=(0.5, 0.5, 0.5, 1))
        
        # Bind buttons to screen changes
        self.nav_buttons['weather'].bind(on_press=lambda x: self.change_screen('weather'))
        self.nav_buttons['screensaver'].bind(on_press=lambda x: self.change_screen('screensaver'))
        self.nav_buttons['spotify'].bind(on_press=lambda x: self.change_screen('spotify'))
        self.nav_buttons['settings'].bind(on_press=lambda x: self.change_screen('settings'))
        
        # Add buttons to navigation bar
        for screen_name, button in self.nav_buttons.items():
            nav_bar.add_widget(button)
        
        # Add navigation bar to root layout
        root.add_widget(nav_bar)
        
        # Start with weather screen
        self.sm.current = 'weather'
        
        # Force a screen refresh to ensure proper rendering
        Clock.schedule_once(self.force_refresh, 0.1)
        
        # Initialize navigation button states
        self._update_nav_buttons()
        
        # Schedule initial tasks
        Clock.schedule_once(self.check_wifi_connection, 1)
        Clock.schedule_interval(self.update_sensor_data, 60)  # Every minute
        Clock.schedule_interval(self.check_screensaver, 10)  # Every 10 seconds
        Clock.schedule_interval(self.update_weather_periodic, self.weather_update_interval)  # Every 30 minutes
        
        # Register touch event to reset screensaver timer
        Window.bind(on_touch_down=self.on_touch)
        
        # Initialize Spotify manager with a delay to ensure UI is ready
        Clock.schedule_once(self.init_spotify_manager, 2)  # 2 second delay
        
        # Start photo sync in a separate thread
        threading.Thread(target=self.photo_manager.sync_photos, daemon=True).start()
        
        Logger.info("SmartDisplay: Application started")
        return root
    
    def on_touch(self, instance, touch):
        """Handle touch events to reset screensaver timer"""
        Window.last_touch_time = time.time()
        return False  # Continue event propagation
    
    def check_wifi_connection(self, dt):
        """Check if WiFi is connected, if not, show WiFi screen"""
        Logger.info("SmartDisplay: Checking WiFi connection")
        if not self.wifi_manager.is_connected():
            Logger.info("SmartDisplay: WiFi not connected, showing WiFi screen")
            self.sm.current = 'wifi'
        else:
            # WiFi is connected, get location and weather
            Logger.info("SmartDisplay: WiFi connected, getting location and weather")
            self.get_location_and_weather()
    
    def get_location_and_weather(self):
        """Get location and weather data"""
        def on_location_success(location):
            Logger.info(f"SmartDisplay: Location obtained: {location['city']}, {location['country']}")
            self.weather_manager.update_weather(location)
            
            # Update weather screen
            weather_screen = self.sm.get_screen('weather')
            weather_data = self.weather_manager.get_weather_data()
            if weather_data:
                weather_screen.update_weather_data(weather_data)
        
        def on_location_failure():
            # Show manual location input on the weather screen
            Logger.warning("SmartDisplay: Failed to get location, showing manual input")
            weather_screen = self.sm.get_screen('weather')
            weather_screen.show_location_input()
        
        self.location_manager.get_location(on_location_success, on_location_failure)
    
    def update_weather_periodic(self, dt):
        """Update weather data periodically"""
        Logger.info("SmartDisplay: Periodic weather update")
        self.get_location_and_weather()
    
    def update_sensor_data(self, dt):
        """Update sensor data from BME680"""
        sensor_data = self.sensor_manager.get_sensor_data()
        Logger.debug(f"SmartDisplay: Sensor data updated: {sensor_data}")
        
        if self.sm.current == 'weather':
            weather_screen = self.sm.get_screen('weather')
            weather_screen.update_sensor_data(sensor_data)
    
    def check_screensaver(self, dt):
        """Check if screensaver should be activated"""
        if self.sm.current not in ['screensaver', 'wifi'] and not self.is_spotify_playing:
            # Get last touch time from Window
            last_touch_time = Window.last_touch_time
            current_time = time.time()
            
            if current_time - last_touch_time > self.screensaver_timeout:
                Logger.info("SmartDisplay: Activating screensaver")
                self.sm.current = 'screensaver'
    
    def on_spotify_status_change(self, is_playing, track_info=None):
        """Handle Spotify status changes"""
        self.is_spotify_playing = is_playing
        
        # Guard against early callback before sm is initialized
        if not hasattr(self, 'sm'):
            Logger.warning("SmartDisplay: Screen manager not initialized yet, ignoring Spotify status change")
            return
        
        if is_playing and track_info:
            Logger.info(f"SmartDisplay: Spotify playing: {track_info['name']} by {track_info['artist']}")
            spotify_screen = self.sm.get_screen('spotify')
            spotify_screen.update_track_info(track_info)
            
            # Only switch to Spotify screen if not in screensaver
            if self.sm.current != 'screensaver':
                self.sm.current = 'spotify'
        elif not is_playing and self.sm.current == 'spotify':
            Logger.info("SmartDisplay: Spotify stopped, returning to weather screen")
            self.sm.current = 'weather'
    
    def change_screen(self, screen_name):
        """Change to the specified screen"""
        Logger.info(f"SmartDisplay: Changing to {screen_name} screen")
        if self.sm.current != screen_name:
            self.sm.current = screen_name
            
            # Update navigation buttons visibility
            self._update_nav_buttons()
    
    def _update_nav_buttons(self):
        """Update navigation buttons visibility based on current screen"""
        if not hasattr(self, 'nav_buttons') or not self.nav_buttons:
            return
            
        current_screen = self.sm.current
        for screen_name, button in self.nav_buttons.items():
            # Special case for screensaver which is named differently in nav buttons
            if current_screen == screen_name:
                button.opacity = 0.3  # Make current screen button semi-transparent
                button.disabled = True  # Disable the button
            else:
                button.opacity = 1.0  # Make other buttons fully visible
                button.disabled = False  # Enable the button
    
    
    def force_refresh(self, dt):
        """Force a screen refresh to ensure proper rendering"""
        Logger.info("SmartDisplay: Forcing screen refresh")
        # Switch to another screen and back to force a complete redraw
        current = self.sm.current
        temp_screen = 'settings' if current != 'settings' else 'wifi'
        self.sm.current = temp_screen
        Clock.schedule_once(lambda dt: setattr(self.sm, 'current', current), 0.05)
    
    def init_spotify_manager(self, dt):
        """Initialize Spotify manager after UI is ready"""
        Logger.info("SmartDisplay: Initializing Spotify manager")
        self.spotify_manager = SpotifyManager(self.on_spotify_status_change)
        
        # Start Spotify monitoring in a separate thread
        threading.Thread(target=self.spotify_manager.start_monitoring, daemon=True).start()
    
    def open_settings_screen(self):
        """Open the settings screen"""
        Logger.info("SmartDisplay: Opening settings screen")
        self.sm.current = 'settings'
    
    def open_weather_screen(self):
        """Open the weather screen"""
        Logger.info("SmartDisplay: Opening weather screen")
        self.sm.current = 'weather'
    
    def open_spotify_screen(self):
        """Open the Spotify screen"""
        Logger.info("SmartDisplay: Opening Spotify screen")
        self.sm.current = 'spotify'
    
    def on_pause(self):
        """Handle application pause"""
        Logger.info("SmartDisplay: Application paused")
        return True  # Prevent app from closing
    
    def on_resume(self):
        """Handle application resume"""
        Logger.info("SmartDisplay: Application resumed")
        # Reset screensaver timer
        Window.last_touch_time = time.time()
        
        # Update data
        self.update_sensor_data(None)
        self.get_location_and_weather()
    
    def on_stop(self):
        """Handle application stop"""
        Logger.info("SmartDisplay: Application stopping")
        # Clean up resources
        if self.spotify_manager:
            self.spotify_manager.stop_monitoring()
        
        if self.photo_manager:
            self.photo_manager.stop_sync()

if __name__ == '__main__':
    try:
        SmartDisplayApp().run()
    except Exception as e:
        Logger.critical(f"SmartDisplay: Fatal error: {str(e)}")
        # Log to file for debugging
        with open("error_log.txt", "a") as f:
            import traceback
            f.write(f"Error at {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}\n")
            f.write(traceback.format_exc())
            f.write("\n\n")
