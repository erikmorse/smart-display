"""
WiFi Screen Module for Smart Display
Displays available WiFi networks and allows connection
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.app import App

class NetworkButton(Button):
    """Custom button for displaying network information"""
    
    def __init__(self, network, **kwargs):
        """Initialize network button"""
        self.network = network
        
        # Create button text with signal strength indicator
        # Handle both 'strength' and 'signal' keys for compatibility
        strength = network.get('strength', network.get('signal', 50))
        strength_indicator = "▂▄▆█"  # Signal strength bars
        
        # Calculate how many bars to show (0-4)
        bars = int(strength / 25) if strength <= 100 else 4
        strength_text = strength_indicator[:bars]
        
        # Add lock symbol if secured
        # Handle both 'secured' and 'security' keys for compatibility
        is_secured = network.get('secured', False)
        if not is_secured and 'security' in network:
            is_secured = network['security'] != 'Open'
        
        if is_secured:
            strength_text += " 🔒"
        
        button_text = f"{network['ssid']} {strength_text}"
        
        super(NetworkButton, self).__init__(text=button_text, size_hint_y=None, height=50, **kwargs)

class WiFiScreen(Screen):
    """WiFi Screen for displaying available networks and connecting"""
    
    def __init__(self, **kwargs):
        """Initialize WiFi Screen"""
        super(WiFiScreen, self).__init__(**kwargs)
        self.app = None
        self.networks = []
        Clock.schedule_once(self.on_screen_init, 0)
    
    def on_screen_init(self, dt):
        """Initialize screen after kivy has processed it"""
        # Get app instance
        self.app = App.get_running_app()
        
        # Create layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header
        header = BoxLayout(size_hint=(1, 0.1))
        header.add_widget(Label(text="WiFi Setup", font_size=24))
        refresh_button = Button(text="Refresh", size_hint=(0.2, 1))
        refresh_button.bind(on_press=self.scan_networks)
        header.add_widget(refresh_button)
        
        # Add status message
        self.status_label = Label(text="Scanning for networks...", size_hint=(1, 0.1))
        
        # Add network list in a scroll view
        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.network_list = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.network_list.bind(minimum_height=self.network_list.setter('height'))
        scroll_view.add_widget(self.network_list)
        
        # Add manual connection button
        manual_button = Button(text="Connect Manually", size_hint=(1, 0.1))
        manual_button.bind(on_press=self.show_manual_connection)
        
        # Add all sections to main layout
        layout.add_widget(header)
        layout.add_widget(self.status_label)
        layout.add_widget(scroll_view)
        layout.add_widget(manual_button)
        
        # Add layout to screen
        self.add_widget(layout)
        
        # Schedule network scan
        Clock.schedule_once(self.scan_networks, 1)
    
    def scan_networks(self, instance=None):
        """Scan for available WiFi networks"""
        self.status_label.text = "Scanning for networks..."
        
        # Clear network list
        self.network_list.clear_widgets()
        
        # Schedule actual scan (to allow UI to update)
        Clock.schedule_once(self._do_scan, 0.1)
    
    def _do_scan(self, dt):
        """Perform network scan"""
        if not self.app:
            return
        
        # Scan for networks
        networks = self.app.wifi_manager.scan_networks()
        self.networks = networks
        
        if networks:
            self.status_label.text = f"Found {len(networks)} networks"
            
            # Add network buttons
            for network in networks:
                btn = NetworkButton(network)
                btn.bind(on_press=lambda btn=btn: self.select_network(btn.network))
                self.network_list.add_widget(btn)
        else:
            self.status_label.text = "No networks found"
    
    def select_network(self, network):
        """Handle network selection"""
        # If network is secured, show password input
        # Handle both 'secured' and 'security' keys for compatibility
        is_secured = network.get('secured', False)
        if not is_secured and 'security' in network:
            is_secured = network['security'] != 'Open'
            
        if is_secured:
            self.show_password_input(network)
        else:
            # Connect to open network
            self.connect_to_network(network['ssid'])
    
    def show_password_input(self, network):
        """Show password input popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text=f"Enter password for {network['ssid']}:"))
        
        # Password input
        password_input = TextInput(password=True, multiline=False)
        content.add_widget(password_input)
        
        # Buttons
        buttons = BoxLayout(size_hint=(1, None), height=40)
        cancel_button = Button(text="Cancel")
        connect_button = Button(text="Connect")
        buttons.add_widget(cancel_button)
        buttons.add_widget(connect_button)
        content.add_widget(buttons)
        
        popup = Popup(title=f"Connect to {network['ssid']}", content=content, size_hint=(0.8, 0.4))
        
        # Bind buttons
        cancel_button.bind(on_press=popup.dismiss)
        connect_button.bind(on_press=lambda x: self.connect_to_network(network['ssid'], password_input.text, popup))
        
        popup.open()
    
    def show_manual_connection(self, instance):
        """Show manual connection popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # SSID input
        ssid_box = BoxLayout(size_hint=(1, None), height=40)
        ssid_box.add_widget(Label(text="SSID:", size_hint=(0.3, 1)))
        ssid_input = TextInput(multiline=False)
        ssid_box.add_widget(ssid_input)
        content.add_widget(ssid_box)
        
        # Password input
        password_box = BoxLayout(size_hint=(1, None), height=40)
        password_box.add_widget(Label(text="Password:", size_hint=(0.3, 1)))
        password_input = TextInput(password=True, multiline=False)
        password_box.add_widget(password_input)
        content.add_widget(password_box)
        
        # Buttons
        buttons = BoxLayout(size_hint=(1, None), height=40)
        cancel_button = Button(text="Cancel")
        connect_button = Button(text="Connect")
        buttons.add_widget(cancel_button)
        buttons.add_widget(connect_button)
        content.add_widget(buttons)
        
        popup = Popup(title="Manual Connection", content=content, size_hint=(0.8, 0.4))
        
        # Bind buttons
        cancel_button.bind(on_press=popup.dismiss)
        connect_button.bind(on_press=lambda x: self.connect_to_network(ssid_input.text, password_input.text, popup))
        
        popup.open()
    
    def connect_to_network(self, ssid, password=None, popup=None):
        """Connect to a WiFi network"""
        if not ssid:
            return
        
        # Close popup if provided
        if popup:
            popup.dismiss()
        
        # Show connecting message
        self.status_label.text = f"Connecting to {ssid}..."
        
        # Schedule connection (to allow UI to update)
        Clock.schedule_once(lambda dt: self._do_connect(ssid, password), 0.1)
    
    def _do_connect(self, ssid, password):
        """Perform network connection"""
        if not self.app:
            return
        
        # Connect to network
        success = self.app.wifi_manager.connect_to_network(ssid, password)
        
        if success:
            self.status_label.text = f"Connected to {ssid}"
            
            # Schedule return to main screen
            Clock.schedule_once(self._return_to_main, 3)
        else:
            self.status_label.text = f"Failed to connect to {ssid}"
    
    def _return_to_main(self, dt):
        """Return to main screen after successful connection"""
        if self.app:
            # Get location and weather
            self.app.get_location_and_weather()
            
            # Switch to weather screen
            self.app.sm.current = 'weather'
