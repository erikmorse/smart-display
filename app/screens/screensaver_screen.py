"""
Screensaver Screen Module for Smart Display
Displays a slideshow of images from Google Photos
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.app import App
import random

class ScreensaverScreen(Screen):
    """Screensaver Screen for displaying photo slideshow"""
    
    def __init__(self, **kwargs):
        """Initialize Screensaver Screen"""
        super(ScreensaverScreen, self).__init__(**kwargs)
        self.app = None
        self.current_image = None
        self.next_image = None
        self.slideshow_timer = None
        self.touch_event = None
        Clock.schedule_once(self.on_screen_init, 0)
    
    def on_screen_init(self, dt):
        """Initialize screen after kivy has processed it"""
        # Get app instance
        self.app = App.get_running_app()
        
        # Create layout
        self.layout = FloatLayout()
        
        # Create image widgets
        self.current_image = Image(source="", allow_stretch=True, keep_ratio=True)
        self.next_image = Image(source="", allow_stretch=True, keep_ratio=True, opacity=0)
        
        # Add images to layout
        self.layout.add_widget(self.current_image)
        self.layout.add_widget(self.next_image)
        
        # Add layout to screen
        self.add_widget(self.layout)
        
        # Bind touch events
        self.touch_event = self.layout.bind(on_touch_down=self.on_touch)
    
    def on_enter(self):
        """Called when screen is entered"""
        # Start slideshow
        self.start_slideshow()
    
    def on_leave(self):
        """Called when screen is exited"""
        # Stop slideshow
        self.stop_slideshow()
    
    def start_slideshow(self):
        """Start the slideshow"""
        if not self.app:
            return
        
        # Load first image
        self.load_next_image()
        
        # Start timer for slideshow
        interval = self.app.photo_manager.get_slideshow_interval()
        self.slideshow_timer = Clock.schedule_interval(self.load_next_image, interval)
    
    def stop_slideshow(self):
        """Stop the slideshow"""
        if self.slideshow_timer:
            self.slideshow_timer.cancel()
            self.slideshow_timer = None
    
    def load_next_image(self, dt=None):
        """Load the next image in the slideshow"""
        if not self.app:
            return
        
        # Get next photo
        photo_path = self.app.photo_manager.get_next_photo()
        
        if not photo_path:
            return
        
        # Swap images
        self.current_image, self.next_image = self.next_image, self.current_image
        
        # Set new image source
        self.next_image.source = photo_path
        self.next_image.opacity = 0
        
        # Choose a random transition
        transition = random.choice(['fade', 'slide_left', 'slide_right', 'slide_up', 'slide_down'])
        
        # Apply transition animation
        if transition == 'fade':
            # Simple fade transition
            anim_out = Animation(opacity=0, duration=1)
            anim_in = Animation(opacity=1, duration=1)
            
            anim_out.start(self.current_image)
            anim_in.start(self.next_image)
            
        else:
            # Slide transitions
            pos = {}
            
            if transition == 'slide_left':
                pos = {'x': -Window.width}
            elif transition == 'slide_right':
                pos = {'x': Window.width}
            elif transition == 'slide_up':
                pos = {'y': Window.height}
            elif transition == 'slide_down':
                pos = {'y': -Window.height}
            
            # Set initial position for next image
            self.next_image.opacity = 1
            self.next_image.pos = (pos.get('x', 0), pos.get('y', 0))
            
            # Animate both images
            anim_out = Animation(pos=(-pos.get('x', 0), -pos.get('y', 0)), duration=1)
            anim_in = Animation(pos=(0, 0), duration=1)
            
            anim_out.start(self.current_image)
            anim_in.start(self.next_image)
    
    def on_touch(self, instance, touch):
        """Handle touch events"""
        # Exit screensaver on touch
        if self.app:
            self.app.sm.current = 'weather'
            return True
        
        return False
