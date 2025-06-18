"""
Location Manager Module for Smart Display
Handles geolocation using Google Geolocation API
"""
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LocationManager:
    """Manages location detection using Google Geolocation API"""
    
    def __init__(self):
        """Initialize Location Manager"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'config', 'location.json')
        self.location = self.load_saved_location()
    
    def load_saved_location(self):
        """Load saved location from config file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading saved location: {e}")
                return None
        return None
    
    def save_location(self, location):
        """Save location to config file"""
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(location, f)
        
        self.location = location
    
    def get_location(self, success_callback, failure_callback):
        """Get location using Google Geolocation API"""
        # If we have a saved location, use it
        if self.location:
            success_callback(self.location)
            return
        
        # If we don't have an API key, fail
        if not self.api_key:
            print("No Google API key found. Set GOOGLE_API_KEY in .env file.")
            failure_callback()
            return
        
        try:
            # Get WiFi access points for geolocation
            wifi_data = self._get_wifi_data()
            
            # If we have WiFi data, use it for geolocation
            if wifi_data:
                url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={self.api_key}"
                
                payload = {
                    "wifiAccessPoints": wifi_data
                }
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    location = {
                        'lat': data['location']['lat'],
                        'lng': data['location']['lng'],
                        'accuracy': data['accuracy']
                    }
                    
                    # Save the location
                    self.save_location(location)
                    
                    # Call success callback
                    success_callback(location)
                    return
            
            # If we get here, we failed to get location
            failure_callback()
            
        except Exception as e:
            print(f"Error getting location: {e}")
            failure_callback()
    
    def _get_wifi_data(self):
        """Get WiFi access point data for geolocation"""
        try:
            # Try to use NetworkManager
            import NetworkManager as nm
            
            wifi_data = []
            
            # Get all WiFi devices
            wifi_devices = [d for d in nm.NetworkManager.GetDevices() 
                           if d.DeviceType == nm.NM_DEVICE_TYPE_WIFI]
            
            if not wifi_devices:
                return None
            
            # Use the first WiFi device
            wifi_device = wifi_devices[0]
            
            # Get access points
            access_points = wifi_device.GetAccessPoints()
            
            for ap in access_points:
                mac = ap.HwAddress
                signal = ap.Strength
                
                if mac and signal:
                    wifi_data.append({
                        "macAddress": mac,
                        "signalStrength": signal
                    })
            
            return wifi_data if wifi_data else None
            
        except Exception as e:
            print(f"Error getting WiFi data: {e}")
            
            # Fallback to using iwlist
            return self._fallback_get_wifi_data()
    
    def _fallback_get_wifi_data(self):
        """Fallback method to get WiFi data using iwlist"""
        try:
            import subprocess
            
            # Run iwlist scan
            result = subprocess.run(['iwlist', 'wlan0', 'scan'], 
                                   capture_output=True, text=True)
            
            if result.returncode != 0:
                return None
            
            # Parse output
            output = result.stdout
            wifi_data = []
            
            # Extract MAC addresses and signal strengths
            import re
            
            # Find all cells
            cells = re.findall(r'Cell \d+ - Address: ([\w:]+).*?Signal level=([-\d]+)', 
                              output, re.DOTALL)
            
            for mac, signal in cells:
                # Convert signal to dBm if needed
                try:
                    signal_strength = int(signal)
                    
                    wifi_data.append({
                        "macAddress": mac,
                        "signalStrength": signal_strength
                    })
                except ValueError:
                    pass
            
            return wifi_data if wifi_data else None
            
        except Exception as e:
            print(f"Error in fallback WiFi data: {e}")
            return None
    
    def set_manual_location(self, city, country):
        """Set location manually using city and country"""
        try:
            if not self.api_key:
                print("No Google API key found. Set GOOGLE_API_KEY in .env file.")
                return False
            
            # Use Google Geocoding API to get coordinates
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city},{country}&key={self.api_key}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    result = data['results'][0]
                    location = {
                        'lat': result['geometry']['location']['lat'],
                        'lng': result['geometry']['location']['lng'],
                        'city': city,
                        'country': country
                    }
                    
                    # Save the location
                    self.save_location(location)
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error setting manual location: {e}")
            return False
