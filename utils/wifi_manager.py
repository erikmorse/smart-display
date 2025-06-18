"""
WiFi Manager Module for Smart Display
Handles WiFi scanning, connection, and management
"""
import os
import subprocess
import json
import time
import platform

# Check if we're on Windows for testing
IS_WINDOWS = platform.system() == 'Windows'

# Try to import NetworkManager, use mock version if not available
try:
    import NetworkManager as nm
except ImportError:
    # Mock NetworkManager for Windows testing
    class MockNetworkManager:
        NM_DEVICE_TYPE_WIFI = 2
        NM_DEVICE_STATE_ACTIVATED = 100
        NM_802_11_AP_FLAGS_PRIVACY = 1
        
        class NetworkManager:
            @staticmethod
            def GetDevices():
                return [MockDevice()]
            
            @staticmethod
            def ActivateConnection(connection, device, specific_object):
                print(f"Mock: Activating connection {connection}")
                return True
        
        class Settings:
            @staticmethod
            def ListConnections():
                return [MockConnection()]
            
            @staticmethod
            def AddConnection(settings):
                print(f"Mock: Adding connection {settings.get('connection', {}).get('id', 'unknown')}")
                return MockConnection()
    
    class MockDevice:
        def __init__(self):
            self.DeviceType = MockNetworkManager.NM_DEVICE_TYPE_WIFI
            self.State = MockNetworkManager.NM_DEVICE_STATE_ACTIVATED
            self.ActiveConnection = MockActiveConnection()
        
        def GetAccessPoints(self):
            return [
                MockAccessPoint("Home WiFi", 90),
                MockAccessPoint("Neighbor's WiFi", 70),
                MockAccessPoint("Coffee Shop", 50),
                MockAccessPoint("Guest Network", 30),
            ]
        
        def RequestScan(self, options):
            pass
    
    class MockAccessPoint:
        def __init__(self, ssid, strength):
            self.Ssid = ssid
            self.Strength = strength
            self.Flags = MockNetworkManager.NM_802_11_AP_FLAGS_PRIVACY
    
    class MockConnection:
        def __init__(self):
            pass
        
        def GetSettings(self):
            return {
                'connection': {'id': 'Home WiFi'},
                '802-11-wireless': {'ssid': 'Home WiFi'}
            }
        
        def Update(self, settings):
            pass
        
        def UpdateSecrets(self, setting_name, secrets):
            pass
    
    class MockActiveConnection:
        def __init__(self):
            self.Connection = MockConnection()
    
    # Use the mock
    nm = MockNetworkManager

class WiFiManager:
    """Manages WiFi connections using NetworkManager"""
    
    def __init__(self):
        """Initialize WiFi Manager"""
        self.available_networks = []
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'config', 'wifi_networks.json')
        self.load_saved_networks()
    
    def load_saved_networks(self):
        """Load saved WiFi networks from config file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.saved_networks = json.load(f)
            except Exception as e:
                print(f"Error loading saved networks: {e}")
                self.saved_networks = {}
        else:
            self.saved_networks = {}
    
    def save_network(self, ssid, password):
        """Save a WiFi network to the config file"""
        self.saved_networks[ssid] = {'password': password}
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(self.saved_networks, f)
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        try:
            # Get all WiFi devices
            wifi_devices = [d for d in nm.NetworkManager.GetDevices() 
                           if d.DeviceType == nm.NM_DEVICE_TYPE_WIFI]
            
            if not wifi_devices:
                print("No WiFi devices found")
                return []
            
            # Use the first WiFi device
            wifi_device = wifi_devices[0]
            
            # Request a scan
            try:
                wifi_device.RequestScan({})
                # Wait for scan to complete
                time.sleep(5)
            except Exception as e:
                print(f"Error requesting scan: {e}")
            
            # Get access points
            access_points = wifi_device.GetAccessPoints()
            
            # Format network information
            self.available_networks = []
            for ap in access_points:
                ssid = ap.Ssid
                if ssid:  # Only include APs with SSIDs
                    strength = ap.Strength
                    secured = ap.Flags & nm.NM_802_11_AP_FLAGS_PRIVACY
                    self.available_networks.append({
                        'ssid': ssid,
                        'strength': strength,
                        'secured': secured
                    })
            
            # Sort by signal strength
            self.available_networks.sort(key=lambda x: x['strength'], reverse=True)
            
            return self.available_networks
            
        except Exception as e:
            print(f"Error scanning networks: {e}")
            # Fallback to using wpa_cli
            return self._fallback_scan_networks()
    
    def _fallback_scan_networks(self):
        """Fallback method to scan networks using wpa_cli"""
        try:
            # Scan for networks
            subprocess.run(['wpa_cli', 'scan'], check=True)
            time.sleep(5)  # Wait for scan to complete
            
            # Get scan results
            result = subprocess.run(['wpa_cli', 'scan_results'], 
                                   capture_output=True, text=True, check=True)
            
            # Parse scan results
            lines = result.stdout.strip().split('\n')[1:]  # Skip header line
            networks = []
            
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 5:
                    bssid, signal, flags, freq, ssid = parts[:5]
                    networks.append({
                        'ssid': ssid,
                        'strength': int(signal) + 100,  # Convert dBm to percentage-like value
                        'secured': '[WPA' in flags or '[WEP' in flags
                    })
            
            # Sort by signal strength
            networks.sort(key=lambda x: x['strength'], reverse=True)
            
            # Remove duplicates (same SSID)
            seen_ssids = set()
            unique_networks = []
            for network in networks:
                if network['ssid'] not in seen_ssids:
                    seen_ssids.add(network['ssid'])
                    unique_networks.append(network)
            
            self.available_networks = unique_networks
            return self.available_networks
            
        except Exception as e:
            print(f"Error in fallback network scan: {e}")
            return []
    
    def connect_to_network(self, ssid, password=None):
        """Connect to a WiFi network"""
        try:
            # Find the device
            wifi_devices = [d for d in nm.NetworkManager.GetDevices() 
                           if d.DeviceType == nm.NM_DEVICE_TYPE_WIFI]
            
            if not wifi_devices:
                print("No WiFi devices found")
                return False
            
            wifi_device = wifi_devices[0]
            
            # Check if we already have a connection for this network
            connections = nm.Settings.ListConnections()
            existing_connection = None
            
            for conn in connections:
                settings = conn.GetSettings()
                if 'connection' in settings and 'id' in settings['connection']:
                    if settings['connection']['id'] == ssid:
                        existing_connection = conn
                        break
            
            # If we have an existing connection, update it
            if existing_connection:
                settings = existing_connection.GetSettings()
                if password:
                    # Update password
                    secrets = {'psk': password}
                    existing_connection.Update(settings)
                    existing_connection.UpdateSecrets('802-11-wireless-security', secrets)
                
                # Activate the connection
                nm.NetworkManager.ActivateConnection(existing_connection, wifi_device, "/")
                
            else:
                # Create a new connection
                settings = {
                    'connection': {
                        'id': ssid,
                        'type': '802-11-wireless',
                        'autoconnect': True
                    },
                    '802-11-wireless': {
                        'ssid': ssid,
                        'mode': 'infrastructure',
                    }
                }
                
                # Add security settings if password provided
                if password:
                    settings['802-11-wireless-security'] = {
                        'key-mgmt': 'wpa-psk',
                        'psk': password
                    }
                
                # Add the connection
                new_connection = nm.Settings.AddConnection(settings)
                
                # Activate the connection
                nm.NetworkManager.ActivateConnection(new_connection, wifi_device, "/")
            
            # Save the network credentials
            if password:
                self.save_network(ssid, password)
            
            return True
            
        except Exception as e:
            print(f"Error connecting to network: {e}")
            # Fallback to wpa_cli
            return self._fallback_connect_to_network(ssid, password)
    
    def _fallback_connect_to_network(self, ssid, password=None):
        """Fallback method to connect to a network using wpa_cli"""
        try:
            # Generate a network configuration
            network_config = f'network={{\n  ssid="{ssid}"\n'
            
            if password:
                network_config += f'  psk="{password}"\n'
            else:
                network_config += '  key_mgmt=NONE\n'
            
            network_config += '}\n'
            
            # Write to a temporary file
            temp_file = '/tmp/wpa_supplicant_network.conf'
            with open(temp_file, 'w') as f:
                f.write(network_config)
            
            # Add the network to wpa_supplicant
            subprocess.run(['wpa_cli', 'add_network'], check=True)
            network_id = subprocess.run(['wpa_cli', 'list_networks'], 
                                       capture_output=True, text=True, check=True)
            
            # Get the last network ID
            lines = network_id.stdout.strip().split('\n')
            if len(lines) < 2:
                return False
                
            last_line = lines[-1]
            network_id = last_line.split('\t')[0]
            
            # Set the network parameters
            subprocess.run(['wpa_cli', 'set_network', network_id, 'ssid', f'"{ssid}"'], check=True)
            
            if password:
                subprocess.run(['wpa_cli', 'set_network', network_id, 'psk', f'"{password}"'], check=True)
            else:
                subprocess.run(['wpa_cli', 'set_network', network_id, 'key_mgmt', 'NONE'], check=True)
            
            # Enable and select the network
            subprocess.run(['wpa_cli', 'enable_network', network_id], check=True)
            subprocess.run(['wpa_cli', 'select_network', network_id], check=True)
            
            # Save the configuration
            subprocess.run(['wpa_cli', 'save_config'], check=True)
            
            # Save the network credentials
            if password:
                self.save_network(ssid, password)
            
            return True
            
        except Exception as e:
            print(f"Error in fallback network connection: {e}")
            return False
    
    def is_connected(self):
        """Check if WiFi is connected"""
        try:
            # Check if any device is connected
            for device in nm.NetworkManager.GetDevices():
                if device.DeviceType == nm.NM_DEVICE_TYPE_WIFI and device.State == nm.NM_DEVICE_STATE_ACTIVATED:
                    return True
            return False
        except Exception as e:
            print(f"Error checking connection status: {e}")
            # Fallback to checking with wpa_cli
            return self._fallback_is_connected()
    
    def _fallback_is_connected(self):
        """Fallback method to check connection using wpa_cli"""
        try:
            result = subprocess.run(['wpa_cli', 'status'], 
                                   capture_output=True, text=True, check=True)
            
            # Check if wpa_state is COMPLETED
            for line in result.stdout.strip().split('\n'):
                if line.startswith('wpa_state='):
                    state = line.split('=')[1]
                    return state == 'COMPLETED'
            
            return False
        except Exception as e:
            print(f"Error in fallback connection check: {e}")
            return False
    
    def get_current_network(self):
        """Get the currently connected network"""
        try:
            for device in nm.NetworkManager.GetDevices():
                if device.DeviceType == nm.NM_DEVICE_TYPE_WIFI and device.State == nm.NM_DEVICE_STATE_ACTIVATED:
                    active_connection = device.ActiveConnection
                    if active_connection:
                        connection = active_connection.Connection
                        settings = connection.GetSettings()
                        if '802-11-wireless' in settings and 'ssid' in settings['802-11-wireless']:
                            return settings['802-11-wireless']['ssid']
            return None
        except Exception as e:
            print(f"Error getting current network: {e}")
            # Fallback to wpa_cli
            return self._fallback_get_current_network()
    
    def _fallback_get_current_network(self):
        """Fallback method to get current network using wpa_cli"""
        try:
            result = subprocess.run(['wpa_cli', 'status'], 
                                   capture_output=True, text=True, check=True)
            
            # Get the ssid
            for line in result.stdout.strip().split('\n'):
                if line.startswith('ssid='):
                    return line.split('=')[1]
            
            return None
        except Exception as e:
            print(f"Error in fallback get current network: {e}")
            return None
