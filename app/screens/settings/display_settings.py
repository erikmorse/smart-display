"""
Display settings component for the Smart Display application
"""
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

class DisplaySettingsPanel(BoxLayout):
    """Display settings panel component"""
    
    def __init__(self, app_instance, **kwargs):
        """Initialize display settings panel"""
        super(DisplaySettingsPanel, self).__init__(orientation='vertical', **kwargs)
        self.app = app_instance
        
        # Create display settings grid
        display_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 1))
        
        # Screensaver timeout
        display_grid.add_widget(Label(text="Screensaver Timeout (minutes):"))
        timeout_box = BoxLayout()
        self.timeout_slider = Slider(min=1, max=30, value=5, step=1)
        self.timeout_label = Label(text=str(int(self.timeout_slider.value)))
        self.timeout_slider.bind(value=self.on_timeout_change)
        timeout_box.add_widget(self.timeout_slider)
        timeout_box.add_widget(self.timeout_label)
        display_grid.add_widget(timeout_box)
        
        # Google Photos album ID
        display_grid.add_widget(Label(text="Google Photos Album ID:"))
        album_box = BoxLayout()
        self.album_input = TextInput(multiline=False)
        album_set_button = Button(text="Set", size_hint=(0.3, 1))
        album_set_button.bind(on_press=self.set_album_id)
        album_box.add_widget(self.album_input)
        album_box.add_widget(album_set_button)
        display_grid.add_widget(album_box)
        
        # Slideshow interval
        display_grid.add_widget(Label(text="Slideshow Interval (seconds):"))
        slideshow_box = BoxLayout()
        self.slideshow_slider = Slider(min=5, max=60, value=30, step=5)
        self.slideshow_label = Label(text=str(int(self.slideshow_slider.value)))
        self.slideshow_slider.bind(value=self.on_slideshow_change)
        slideshow_box.add_widget(self.slideshow_slider)
        slideshow_box.add_widget(self.slideshow_label)
        display_grid.add_widget(slideshow_box)
        
        # Add grid to panel
        self.add_widget(display_grid)
        
        # Load current display settings
        self.load_display_settings()
    
    def load_display_settings(self):
        """Load current display settings"""
        if not self.app:
            return
        
        # Load screensaver timeout
        self.timeout_slider.value = self.app.screensaver_timeout / 60  # Convert seconds to minutes
        
        # Load Google Photos album ID
        if hasattr(self.app, 'photo_manager'):
            self.album_input.text = self.app.photo_manager.config.get('album_id', '')
            self.slideshow_slider.value = self.app.photo_manager.config.get('slideshow_interval', 30)
    
    def on_timeout_change(self, instance, value):
        """Handle screensaver timeout change"""
        # Update label
        self.timeout_label.text = str(int(value))
        
        # Update app setting
        if self.app:
            self.app.screensaver_timeout = int(value) * 60  # Convert minutes to seconds
    
    def on_slideshow_change(self, instance, value):
        """Handle slideshow interval change"""
        # Update label
        self.slideshow_label.text = str(int(value))
        
        # Update app setting
        if self.app and hasattr(self.app, 'photo_manager'):
            self.app.photo_manager.set_slideshow_interval(int(value))
    
    def set_album_id(self, instance):
        """Set Google Photos album ID"""
        if self.app and hasattr(self.app, 'photo_manager'):
            self.app.photo_manager.set_album_id(self.album_input.text)
            self.show_message("Album ID set successfully")
    
    def show_message(self, message):
        """Show a message popup"""
        popup = Popup(title='Message', content=Label(text=message),
                     size_hint=(0.6, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
