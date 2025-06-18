"""
Mock NetworkManager module for Windows testing
"""

# Mock NetworkManager constants
NM_STATE_UNKNOWN = 0
NM_STATE_ASLEEP = 10
NM_STATE_DISCONNECTED = 20
NM_STATE_DISCONNECTING = 30
NM_STATE_CONNECTING = 40
NM_STATE_CONNECTED_LOCAL = 50
NM_STATE_CONNECTED_SITE = 60
NM_STATE_CONNECTED_GLOBAL = 70

# Mock NetworkManager device types
NM_DEVICE_TYPE_UNKNOWN = 0
NM_DEVICE_TYPE_ETHERNET = 1
NM_DEVICE_TYPE_WIFI = 2
NM_DEVICE_TYPE_MODEM = 8

# Mock NetworkManager device states
NM_DEVICE_STATE_UNKNOWN = 0
NM_DEVICE_STATE_UNMANAGED = 10
NM_DEVICE_STATE_UNAVAILABLE = 20
NM_DEVICE_STATE_DISCONNECTED = 30
NM_DEVICE_STATE_PREPARE = 40
NM_DEVICE_STATE_CONFIG = 50
NM_DEVICE_STATE_NEED_AUTH = 60
NM_DEVICE_STATE_IP_CONFIG = 70
NM_DEVICE_STATE_IP_CHECK = 80
NM_DEVICE_STATE_SECONDARIES = 90
NM_DEVICE_STATE_ACTIVATED = 100
NM_DEVICE_STATE_DEACTIVATING = 110
NM_DEVICE_STATE_FAILED = 120

# Mock NetworkManager classes
class NetworkManager:
    """Mock NetworkManager class"""
    
    @staticmethod
    def GetDevices():
        """Get all network devices"""
        return [MockWifiDevice()]
    
    @staticmethod
    def GetAllDevices():
        """Get all network devices"""
        return [MockWifiDevice()]
    
    @staticmethod
    def NetworkingEnabled():
        """Check if networking is enabled"""
        return True
    
    @staticmethod
    def WirelessEnabled():
        """Check if wireless is enabled"""
        return True
    
    @staticmethod
    def State():
        """Get current network state"""
        return NM_STATE_CONNECTED_GLOBAL

class Settings:
    """Mock NetworkManager Settings class"""
    
    @staticmethod
    def ListConnections():
        """List all connections"""
        return [MockConnection()]
    
    @staticmethod
    def AddConnection(settings):
        """Add a new connection"""
        return MockConnection()

class MockWifiDevice:
    """Mock WiFi device"""
    
    def __init__(self):
        self.DeviceType = NM_DEVICE_TYPE_WIFI
        self.State = NM_DEVICE_STATE_ACTIVATED
        self.ActiveConnection = MockActiveConnection()
        self.Managed = True
        self.Interface = "wlan0"
    
    def GetAccessPoints(self):
        """Get available access points"""
        return [
            MockAccessPoint("Home WiFi", 90),
            MockAccessPoint("Neighbor's WiFi", 70),
            MockAccessPoint("Coffee Shop", 50),
            MockAccessPoint("Guest Network", 30),
        ]
    
    def RequestScan(self, options=None):
        """Request a network scan"""
        pass
    
    def SpecificDevice(self):
        """Get specific device"""
        return self

class MockAccessPoint:
    """Mock WiFi access point"""
    
    def __init__(self, ssid, strength):
        self.Ssid = ssid.encode('utf-8')
        self.Strength = strength
        self.WpaFlags = 1
        self.RsnFlags = 1
        self.Flags = 1
    
    def GetFlags(self):
        """Get flags"""
        return self.Flags
    
    def GetWpaFlags(self):
        """Get WPA flags"""
        return self.WpaFlags
    
    def GetRsnFlags(self):
        """Get RSN flags"""
        return self.RsnFlags

class MockConnection:
    """Mock connection"""
    
    def __init__(self):
        self.Id = "mock-connection"
        self.Uuid = "00000000-0000-0000-0000-000000000000"
        self.Type = "802-11-wireless"
    
    def GetSettings(self):
        """Get connection settings"""
        return {
            "connection": {
                "id": self.Id,
                "uuid": self.Uuid,
                "type": self.Type
            },
            "802-11-wireless": {
                "ssid": "Home WiFi".encode('utf-8'),
                "mode": "infrastructure"
            }
        }
    
    def Update(self, settings):
        """Update connection settings"""
        pass
    
    def Delete(self):
        """Delete connection"""
        pass

class MockActiveConnection:
    """Mock active connection"""
    
    def __init__(self):
        self.Connection = MockConnection()
        self.State = 2  # Active
        self.Type = "802-11-wireless"
    
    def GetSpecificObject(self):
        """Get specific object"""
        return MockAccessPoint("Home WiFi", 90)
