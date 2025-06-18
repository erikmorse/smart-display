"""
API settings component for the Smart Display application
"""
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

class ApiSettingsPanel(BoxLayout):
    """API settings panel component"""
    
    def __init__(self, app_instance, **kwargs):
        """Initialize API settings panel"""
        super(ApiSettingsPanel, self).__init__(orientation='vertical', **kwargs)
        self.app = app_instance
        
        # Create API settings grid
        api_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 1))
        
        # API Keys section
        api_grid.add_widget(Label(text="API Keys:", font_size=18))
        api_grid.add_widget(Label(text=""))  # Empty cell for alignment
        
        # Google API Key
        api_grid.add_widget(Label(text="Google API Key:"))
        google_box = BoxLayout()
        self.google_input = TextInput(multiline=False, password=True)
        google_set_button = Button(text="Set", size_hint=(0.3, 1))
        google_set_button.bind(on_press=lambda x: self.set_api_key('GOOGLE_API_KEY', self.google_input.text))
        google_box.add_widget(self.google_input)
        google_box.add_widget(google_set_button)
        api_grid.add_widget(google_box)
        
        # OpenWeatherMap API Key
        api_grid.add_widget(Label(text="OpenWeatherMap API Key:"))
        weather_box = BoxLayout()
        self.weather_input = TextInput(multiline=False, password=True)
        weather_set_button = Button(text="Set", size_hint=(0.3, 1))
        weather_set_button.bind(on_press=lambda x: self.set_api_key('OPENWEATHERMAP_API_KEY', self.weather_input.text))
        weather_box.add_widget(self.weather_input)
        weather_box.add_widget(weather_set_button)
        api_grid.add_widget(weather_box)
        
        # Add grid to panel
        self.add_widget(api_grid)
        
        # Load current API settings
        self.load_api_settings()
    
    def load_api_settings(self):
        """Load current API settings"""
        # Load API keys from .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        
                        if key == 'GOOGLE_API_KEY':
                            self.google_input.text = value
                        elif key == 'OPENWEATHERMAP_API_KEY':
                            self.weather_input.text = value
    
    def set_api_key(self, key_name, value):
        """Set API key in .env file"""
        if not value.strip():
            return
            
        # Update .env file
        try:
            # Read existing .env file
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
            env_vars = {}
            
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, val = line.strip().split('=', 1)
                            env_vars[key] = val
            
            # Update or add the key
            env_vars[key_name] = value
            
            # Write back to .env file
            with open(env_path, 'w') as f:
                for key, val in env_vars.items():
                    f.write(f"{key}={val}\n")
                    
            # Show confirmation
            self.show_message(f'{key_name} has been set.')
            
        except Exception as e:
            # Show error
            self.show_message(f'Failed to set {key_name}: {str(e)}')
    
    def show_message(self, message):
        """Show a message popup"""
        popup = Popup(title='Message', content=Label(text=message),
                     size_hint=(0.6, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
