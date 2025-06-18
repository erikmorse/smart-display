"""
Sensor Manager Module for Smart Display
Handles BME680 environmental sensor data
"""
import os
import json
import time
from datetime import datetime

class SensorManager:
    """Manages BME680 environmental sensor data"""
    
    def __init__(self):
        """Initialize Sensor Manager"""
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'config', 'sensor.json')
        self.sensor_data = self.load_saved_data()
        self.last_update = None
        self.sensor = None
        
        # Try to initialize the sensor
        self._init_sensor()
    
    def _init_sensor(self):
        """Initialize the BME680 sensor"""
        try:
            import board
            import adafruit_bme680
            
            # Create sensor object using I2C
            i2c = board.I2C()  # uses board.SCL and board.SDA
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
            
            # Set the temperature compensation (adjust for self-heating)
            self.sensor.temperature_offset = -2.5
            
            print("BME680 sensor initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing BME680 sensor: {e}")
            print("Using simulated sensor data")
            return False
    
    def load_saved_data(self):
        """Load saved sensor data from config file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading saved sensor data: {e}")
                return self._get_default_data()
        return self._get_default_data()
    
    def _get_default_data(self):
        """Get default sensor data (for simulation)"""
        return {
            'temperature': 21.0,
            'humidity': 50.0,
            'pressure': 1013.25,
            'gas': 50000,
            'altitude': 0.0,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_data(self, sensor_data):
        """Save sensor data to config file"""
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(sensor_data, f)
        
        self.sensor_data = sensor_data
        self.last_update = datetime.now()
    
    def get_sensor_data(self):
        """Get sensor data from BME680"""
        # Check if we need to update (less than 1 minute since last update)
        if self.last_update:
            time_since_update = (datetime.now() - self.last_update).total_seconds()
            if time_since_update < 60 and self.sensor_data:
                return self.sensor_data
        
        # If we have a sensor, read from it
        if self.sensor:
            try:
                # Read data from sensor
                data = {
                    'temperature': round(self.sensor.temperature, 1),
                    'humidity': round(self.sensor.relative_humidity, 1),
                    'pressure': round(self.sensor.pressure, 2),
                    'gas': int(self.sensor.gas),
                    'altitude': round(self.sensor.altitude, 1),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Calculate air quality index (simple approximation)
                # Lower gas resistance = more pollutants = worse air quality
                gas_baseline = 100000  # Example baseline, should be calibrated
                gas_score = (data['gas'] / gas_baseline) * 100
                gas_score = min(100, max(0, gas_score))  # Clamp between 0-100
                
                # Add air quality to data
                data['air_quality'] = int(gas_score)
                
                # Save the data
                self.save_data(data)
                
                return data
                
            except Exception as e:
                print(f"Error reading from BME680 sensor: {e}")
                # Fall back to simulated data
                return self._get_simulated_data()
        else:
            # No sensor, use simulated data
            return self._get_simulated_data()
    
    def _get_simulated_data(self):
        """Get simulated sensor data"""
        # Start with the last known data or defaults
        base_data = self.sensor_data if self.sensor_data else self._get_default_data()
        
        # Add small random variations
        import random
        
        data = {
            'temperature': round(base_data['temperature'] + random.uniform(-0.5, 0.5), 1),
            'humidity': round(base_data['humidity'] + random.uniform(-2, 2), 1),
            'pressure': round(base_data['pressure'] + random.uniform(-1, 1), 2),
            'gas': int(base_data['gas'] + random.uniform(-5000, 5000)),
            'altitude': round(base_data['altitude'] + random.uniform(-0.5, 0.5), 1),
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate air quality index (simple approximation)
        gas_baseline = 100000  # Example baseline
        gas_score = (data['gas'] / gas_baseline) * 100
        gas_score = min(100, max(0, gas_score))  # Clamp between 0-100
        
        # Add air quality to data
        data['air_quality'] = int(gas_score)
        
        # Save the data
        self.save_data(data)
        
        return data
