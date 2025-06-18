"""
WiFi settings component for the Smart Display application
"""
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

from .network_components import NetworkButton

class WiFiSettingsPanel(BoxLayout):
    """WiFi settings panel component"""
    
    def __init__(self, app_instance, **kwargs):
        """Initialize WiFi settings panel"""
        super(WiFiSettingsPanel, self).__init__(orientation='vertical', **kwargs)
        self.app = app_instance
        self.networks = []
        
        # Create WiFi settings grid
        wifi_grid = GridLayout(cols=2, spacing=10, size_hint=(1, 1))
        
        # WiFi section header
        wifi_grid.add_widget(Label(text="WiFi Settings:", font_size=18))
        wifi_grid.add_widget(Label(text=""))  # Empty cell for alignment
        
        # WiFi network selection
        wifi_grid.add_widget(Label(text="WiFi Network:"))
        wifi_box = BoxLayout()
        self.wifi_status_label = Label(text="Not connected", size_hint=(0.7, 1))
        wifi_scan_button = Button(text="Scan", size_hint=(0.3, 1))
        wifi_scan_button.bind(on_press=self.show_wifi_networks)
        wifi_box.add_widget(self.wifi_status_label)
        wifi_box.add_widget(wifi_scan_button)
        wifi_grid.add_widget(wifi_box)
        
        # Manual WiFi connection
        wifi_grid.add_widget(Label(text="Connect Manually:"))
        manual_wifi_box = BoxLayout()
        manual_wifi_button = Button(text="Connect", size_hint=(1, 1))
        manual_wifi_button.bind(on_press=self.show_manual_connection)
        manual_wifi_box.add_widget(manual_wifi_button)
        wifi_grid.add_widget(manual_wifi_box)
        
        # Add grid to panel
        self.add_widget(wifi_grid)
        
        # Load current WiFi status
        self.load_wifi_status()
    
    def load_wifi_status(self):
        """Load current WiFi status"""
        if not self.app or not hasattr(self.app, 'wifi_manager'):
            return
            
        try:
            # Get current connection
            current_network = self.app.wifi_manager.get_current_connection()
            if current_network:
                self.wifi_status_label.text = f"Connected to {current_network}"
            else:
                self.wifi_status_label.text = "Not connected"
        except Exception:
            self.wifi_status_label.text = "Status unknown"
    
    def show_wifi_networks(self, instance=None):
        """Show available WiFi networks in a popup"""
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add status label
        status_label = Label(text="Scanning for networks...", size_hint=(1, 0.1))
        
        # Add network list in a scroll view
        scroll_view = ScrollView(size_hint=(1, 0.8))
        network_list = GridLayout(cols=1, spacing=2, size_hint_y=None)
        network_list.bind(minimum_height=network_list.setter('height'))
        scroll_view.add_widget(network_list)
        
        # Add close button
        close_button = Button(text="Close", size_hint=(1, 0.1))
        
        # Add all sections to content
        content.add_widget(status_label)
        content.add_widget(scroll_view)
        content.add_widget(close_button)
        
        # Create and open popup
        popup = Popup(title='WiFi Networks', content=content, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)
        popup.open()
        
        # Scan for networks
        def scan_networks(dt):
            status_label.text = "Scanning for networks..."
            network_list.clear_widgets()
            
            try:
                # Get WiFi manager from app
                wifi_manager = self.app.wifi_manager
                networks = wifi_manager.get_networks()
                self.networks = networks
                
                if networks:
                    status_label.text = f"Found {len(networks)} networks"
                    
                    # Add network buttons
                    for network in networks:
                        network_button = NetworkButton(network)
                        network_button.bind(on_press=lambda btn: self.show_password_input(btn.network, popup))
                        network_list.add_widget(network_button)
                else:
                    status_label.text = "No networks found"
            except Exception as e:
                status_label.text = f"Error: {str(e)}"
        
        # Schedule network scan
        Clock.schedule_once(scan_networks, 0.5)
    
    def show_manual_connection(self, instance=None):
        """Show manual WiFi connection dialog"""
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add input fields
        ssid_box = BoxLayout(size_hint=(1, 0.3))
        ssid_box.add_widget(Label(text="SSID:", size_hint=(0.3, 1)))
        ssid_input = TextInput(multiline=False, size_hint=(0.7, 1))
        ssid_box.add_widget(ssid_input)
        
        password_box = BoxLayout(size_hint=(1, 0.3))
        password_box.add_widget(Label(text="Password:", size_hint=(0.3, 1)))
        password_input = TextInput(multiline=False, password=True, size_hint=(0.7, 1))
        password_box.add_widget(password_input)
        
        # Add buttons
        button_box = BoxLayout(size_hint=(1, 0.3), spacing=10)
        cancel_button = Button(text="Cancel")
        connect_button = Button(text="Connect")
        button_box.add_widget(cancel_button)
        button_box.add_widget(connect_button)
        
        # Add all sections to content
        content.add_widget(ssid_box)
        content.add_widget(password_box)
        content.add_widget(button_box)
        
        # Create and open popup
        popup = Popup(title='Connect to WiFi', content=content, size_hint=(0.8, 0.4))
        cancel_button.bind(on_press=popup.dismiss)
        
        # Connect button action
        def connect_action(btn):
            ssid = ssid_input.text.strip()
            password = password_input.text
            
            if not ssid:
                return
            
            try:
                # Get WiFi manager from app
                wifi_manager = self.app.wifi_manager
                result = wifi_manager.connect(ssid, password)
                
                if result:
                    self.wifi_status_label.text = f"Connected to {ssid}"
                    popup.dismiss()
                    
                    # Save credentials to .env file
                    self.save_wifi_credentials(ssid, password)
                    
                    # Show success popup
                    self.show_message(f'Connected to {ssid}')
                else:
                    # Show error popup
                    self.show_message('Failed to connect')
            except Exception as e:
                # Show error popup
                self.show_message(f'Error: {str(e)}')
        
        connect_button.bind(on_press=connect_action)
        popup.open()
    
    def show_password_input(self, network, parent_popup):
        """Show password input dialog for selected network"""
        # Dismiss parent popup
        parent_popup.dismiss()
        
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add network info
        content.add_widget(Label(text=f"Network: {network['ssid']}", size_hint=(1, 0.3)))
        
        # Add password input if secured
        is_secured = network.get('secured', False)
        if not is_secured and 'security' in network:
            is_secured = network['security'] != 'Open'
        
        password_input = None
        if is_secured:
            password_box = BoxLayout(size_hint=(1, 0.3))
            password_box.add_widget(Label(text="Password:", size_hint=(0.3, 1)))
            password_input = TextInput(multiline=False, password=True, size_hint=(0.7, 1))
            password_box.add_widget(password_input)
            content.add_widget(password_box)
        
        # Add buttons
        button_box = BoxLayout(size_hint=(1, 0.3), spacing=10)
        cancel_button = Button(text="Cancel")
        connect_button = Button(text="Connect")
        button_box.add_widget(cancel_button)
        button_box.add_widget(connect_button)
        content.add_widget(button_box)
        
        # Create and open popup
        popup = Popup(title='Connect to WiFi', content=content, size_hint=(0.8, 0.4))
        cancel_button.bind(on_press=popup.dismiss)
        
        # Connect button action
        def connect_action(btn):
            try:
                # Get WiFi manager from app
                wifi_manager = self.app.wifi_manager
                password = password_input.text if password_input else ""
                result = wifi_manager.connect(network['ssid'], password)
                
                if result:
                    self.wifi_status_label.text = f"Connected to {network['ssid']}"
                    popup.dismiss()
                    
                    # Save credentials to .env file
                    self.save_wifi_credentials(network['ssid'], password)
                    
                    # Show success popup
                    self.show_message(f'Connected to {network["ssid"]}')
                else:
                    # Show error popup
                    self.show_message('Failed to connect')
            except Exception as e:
                # Show error popup
                self.show_message(f'Error: {str(e)}')
        
        connect_button.bind(on_press=connect_action)
        popup.open()
    
    def save_wifi_credentials(self, ssid, password):
        """Save WiFi credentials to .env file"""
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
            
            # Update or add the WiFi credentials
            env_vars['WIFI_SSID'] = ssid
            env_vars['WIFI_PASSWORD'] = password
            
            # Write back to .env file
            with open(env_path, 'w') as f:
                for key, val in env_vars.items():
                    f.write(f"{key}={val}\n")
                    
        except Exception as e:
            # Show error
            self.show_message(f'Failed to save WiFi credentials: {str(e)}')
    
    def show_message(self, message):
        """Show a message popup"""
        popup = Popup(title='Message', content=Label(text=message),
                     size_hint=(0.6, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
