"""
Mock WiFi Manager Module for Smart Display
Used for testing on Windows platforms
"""
import os
import json
import time
import random

class WiFiManager:
    """WiFi Manager class for handling WiFi connections"""
    
    def __init__(self):
        """Initialize WiFi Manager"""
        self.config_file = os.path.join('config', 'wifi.json')
        self.saved_networks = self._load_saved_networks()
        self.current_network = None
        
        # Mock connected state
        self.is_connected_state = True
    
    def _load_saved_networks(self):
        """Load saved networks from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('saved_networks', [])
            except Exception as e:
                print(f"Error loading saved networks: {str(e)}")
        
        # Create default config if it doesn't exist
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump({'saved_networks': []}, f)
        
        return []
    
    def _save_networks(self):
        """Save networks to config file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump({'saved_networks': self.saved_networks}, f)
            return True
        except Exception as e:
            print(f"Error saving networks: {str(e)}")
            return False
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        # Mock network scan
        networks = [
            {"ssid": "Home WiFi", "signal": 90, "security": "WPA2"},
            {"ssid": "Neighbor's WiFi", "signal": 70, "security": "WPA2"},
            {"ssid": "Coffee Shop", "signal": 50, "security": "Open"},
            {"ssid": "Guest Network", "signal": 30, "security": "WEP"},
            {"ssid": "IoT Network", "signal": 85, "security": "WPA2"},
            {"ssid": "5G_Network", "signal": 65, "security": "WPA3"},
        ]
        
        # Add some randomness to signal strength
        for network in networks:
            network["signal"] = min(100, max(0, network["signal"] + random.randint(-10, 10)))
        
        # Sort by signal strength
        networks.sort(key=lambda x: x["signal"], reverse=True)
        
        return networks
    
    def connect_to_network(self, ssid, password=None):
        """Connect to a WiFi network"""
        print(f"Mock connecting to {ssid}" + (f" with password {password}" if password else ""))
        
        # Simulate connection delay
        time.sleep(1)
        
        # Check if network is in saved networks
        network_exists = False
        for network in self.saved_networks:
            if network["ssid"] == ssid:
                network_exists = True
                break
        
        # Add to saved networks if not already saved
        if not network_exists:
            self.saved_networks.append({
                "ssid": ssid,
                "password": password
            })
            self._save_networks()
        
        # Set as current network
        self.current_network = ssid
        self.is_connected_state = True
        
        return True
    
    def disconnect(self):
        """Disconnect from current network"""
        print("Mock disconnecting from network")
        self.current_network = None
        self.is_connected_state = False
        return True
    
    def is_connected(self):
        """Check if connected to a network"""
        return self.is_connected_state
    
    def get_current_network(self):
        """Get current network SSID"""
        return self.current_network
    
    def get_saved_networks(self):
        """Get list of saved networks"""
        return self.saved_networks
    
    def forget_network(self, ssid):
        """Remove a network from saved networks"""
        for i, network in enumerate(self.saved_networks):
            if network["ssid"] == ssid:
                del self.saved_networks[i]
                self._save_networks()
                return True
        
        return False
