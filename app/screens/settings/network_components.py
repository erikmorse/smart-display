"""
Network-related components for the Settings screen
"""
from kivy.uix.button import Button

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
