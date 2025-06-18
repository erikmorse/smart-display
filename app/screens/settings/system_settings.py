"""
System settings component for the Smart Display application
"""
import os
import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock

class SystemSettingsPanel(BoxLayout):
    """System settings panel component"""
    
    def __init__(self, app_instance, **kwargs):
        """Initialize system settings panel"""
        super(SystemSettingsPanel, self).__init__(orientation='vertical', **kwargs)
        self.app = app_instance
        
        # Create system settings grid
        system_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 1))
        
        # System section header
        system_grid.add_widget(Label(text="System:", font_size=18))
        system_grid.add_widget(Label(text=""))  # Empty cell for alignment
        
        # Restart button
        system_grid.add_widget(Label(text="Restart Application:"))
        restart_button = Button(text="Restart")
        restart_button.bind(on_press=self.restart_app)
        system_grid.add_widget(restart_button)
        
        # Add grid to panel
        self.add_widget(system_grid)
    
    def restart_app(self, instance):
        """Restart the application"""
        # Show confirmation dialog
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Are you sure you want to restart the application?"))
        
        buttons = BoxLayout(size_hint=(1, None), height=40)
        cancel_button = Button(text="Cancel")
        restart_button = Button(text="Restart")
        buttons.add_widget(cancel_button)
        buttons.add_widget(restart_button)
        content.add_widget(buttons)
        
        popup = Popup(title="Confirm Restart", content=content, size_hint=(0.8, 0.3))
        
        cancel_button.bind(on_press=popup.dismiss)
        restart_button.bind(on_press=self._do_restart)
        
        popup.open()
    
    def _do_restart(self, instance):
        """Actually restart the application"""
        if self.app:
            self.app.stop()
            
            # Schedule restart
            Clock.schedule_once(lambda dt: os.execv(sys.executable, [sys.executable] + sys.argv), 1)
    
    def show_message(self, message):
        """Show a message popup"""
        popup = Popup(title='Message', content=Label(text=message),
                     size_hint=(0.6, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
