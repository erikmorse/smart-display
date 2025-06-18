"""
Main Settings Screen for Smart Display
Integrates all settings components into a tabbed interface
"""
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock

from .display_settings import DisplaySettingsPanel
from .wifi_settings import WiFiSettingsPanel
from .api_settings import ApiSettingsPanel
from .spotify_settings import SpotifySettingsPanel
from .system_settings import SystemSettingsPanel

class SettingsScreen(Screen):
    """Settings Screen for configuring application settings"""
    
    def __init__(self, **kwargs):
        """Initialize Settings Screen"""
        super(SettingsScreen, self).__init__(**kwargs)
        self.app = None
        Clock.schedule_once(self.on_screen_init, 0)
    
    def on_screen_init(self, dt):
        """Initialize screen after kivy has processed it"""
        # Get app instance
        self.app = App.get_running_app()
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header
        header = BoxLayout(size_hint=(1, 0.1))
        header.add_widget(Label(text="", size_hint=(0.2, 1)))  # Left spacer for alignment
        header.add_widget(Label(text="Settings", font_size=24))
        header.add_widget(Label(text="", size_hint=(0.2, 1)))  # Right spacer for alignment
        
        # Create tabbed panel for settings
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_pos='top_mid', 
                                  size_hint=(1, 0.9), tab_height=60)
        
        # Display tab
        display_tab = TabbedPanelItem(text='Display')
        display_tab.add_widget(DisplaySettingsPanel(self.app))
        tabbed_panel.add_widget(display_tab)
        
        # WiFi tab
        wifi_tab = TabbedPanelItem(text='WiFi')
        wifi_tab.add_widget(WiFiSettingsPanel(self.app))
        tabbed_panel.add_widget(wifi_tab)
        
        # API tab
        api_tab = TabbedPanelItem(text='API Keys')
        api_tab.add_widget(ApiSettingsPanel(self.app))
        tabbed_panel.add_widget(api_tab)
        
        # Spotify tab
        spotify_tab = TabbedPanelItem(text='Spotify')
        spotify_tab.add_widget(SpotifySettingsPanel(self.app))
        tabbed_panel.add_widget(spotify_tab)
        
        # System tab
        system_tab = TabbedPanelItem(text='System')
        system_tab.add_widget(SystemSettingsPanel(self.app))
        tabbed_panel.add_widget(system_tab)
        
        # Set default tab
        tabbed_panel.default_tab = display_tab
        
        # Add components to layout
        layout.add_widget(header)
        layout.add_widget(tabbed_panel)
        
        # Add layout to screen
        self.add_widget(layout)
        
    def go_back(self, instance):
        """Go back to weather screen"""
        if self.app:
            self.app.sm.current = 'weather'
