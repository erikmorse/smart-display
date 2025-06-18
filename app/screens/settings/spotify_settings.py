"""
Spotify settings component for the Smart Display application
"""
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

class SpotifySettingsPanel(BoxLayout):
    """Spotify settings panel component"""
    
    def __init__(self, app_instance, **kwargs):
        """Initialize Spotify settings panel"""
        super(SpotifySettingsPanel, self).__init__(orientation='vertical', **kwargs)
        self.app = app_instance
        
        # Create Spotify settings grid
        spotify_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 1))
        
        # Spotify section header
        spotify_grid.add_widget(Label(text="Spotify Settings:", font_size=18))
        spotify_grid.add_widget(Label(text=""))  # Empty cell for alignment
        
        # Spotify Client ID
        spotify_grid.add_widget(Label(text="Spotify Client ID:"))
        spotify_id_box = BoxLayout()
        self.spotify_id_input = TextInput(multiline=False)
        spotify_id_set_button = Button(text="Set", size_hint=(0.3, 1))
        spotify_id_set_button.bind(on_press=lambda x: self.set_api_key('SPOTIFY_CLIENT_ID', self.spotify_id_input.text))
        spotify_id_box.add_widget(self.spotify_id_input)
        spotify_id_box.add_widget(spotify_id_set_button)
        spotify_grid.add_widget(spotify_id_box)
        
        # Spotify Client Secret
        spotify_grid.add_widget(Label(text="Spotify Client Secret:"))
        spotify_secret_box = BoxLayout()
        self.spotify_secret_input = TextInput(multiline=False, password=True)
        spotify_secret_set_button = Button(text="Set", size_hint=(0.3, 1))
        spotify_secret_set_button.bind(on_press=lambda x: self.set_api_key('SPOTIFY_CLIENT_SECRET', self.spotify_secret_input.text))
        spotify_secret_box.add_widget(self.spotify_secret_input)
        spotify_secret_box.add_widget(spotify_secret_set_button)
        spotify_grid.add_widget(spotify_secret_box)
        
        # Spotify Username
        spotify_grid.add_widget(Label(text="Spotify Username:"))
        spotify_user_box = BoxLayout()
        self.spotify_user_input = TextInput(multiline=False)
        spotify_user_set_button = Button(text="Set", size_hint=(0.3, 1))
        spotify_user_set_button.bind(on_press=lambda x: self.set_api_key('SPOTIFY_USERNAME', self.spotify_user_input.text))
        spotify_user_box.add_widget(self.spotify_user_input)
        spotify_user_box.add_widget(spotify_user_set_button)
        spotify_grid.add_widget(spotify_user_box)
        
        # Spotify Password
        spotify_grid.add_widget(Label(text="Spotify Password:"))
        spotify_pass_box = BoxLayout()
        self.spotify_pass_input = TextInput(multiline=False, password=True)
        spotify_pass_set_button = Button(text="Set", size_hint=(0.3, 1))
        spotify_pass_set_button.bind(on_press=lambda x: self.set_api_key('SPOTIFY_PASSWORD', self.spotify_pass_input.text))
        spotify_pass_box.add_widget(self.spotify_pass_input)
        spotify_pass_box.add_widget(spotify_pass_set_button)
        spotify_grid.add_widget(spotify_pass_box)
        
        # Add grid to panel
        self.add_widget(spotify_grid)
        
        # Load current Spotify settings
        self.load_spotify_settings()
    
    def load_spotify_settings(self):
        """Load current Spotify settings"""
        # Load Spotify settings from .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        
                        if key == 'SPOTIFY_CLIENT_ID':
                            self.spotify_id_input.text = value
                        elif key == 'SPOTIFY_CLIENT_SECRET':
                            self.spotify_secret_input.text = value
                        elif key == 'SPOTIFY_USERNAME':
                            self.spotify_user_input.text = value
                        elif key == 'SPOTIFY_PASSWORD':
                            self.spotify_pass_input.text = value
    
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
