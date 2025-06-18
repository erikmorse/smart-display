"""
Spotify Screen Module for Smart Display
Displays Spotify playback information and controls
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App
from kivy.core.window import Window

class SpotifyScreen(Screen):
    """Spotify Screen for displaying music information and controls"""
    
    # Track properties
    track_name = StringProperty("No Track Playing")
    artist_name = StringProperty("--")
    album_name = StringProperty("--")
    album_art = StringProperty("")
    
    # Progress properties
    progress_text = StringProperty("--:-- / --:--")
    progress_value = ObjectProperty(0)
    
    def __init__(self, **kwargs):
        """Initialize Spotify Screen"""
        super(SpotifyScreen, self).__init__(**kwargs)
        self.app = None
        self.track_info = None
        self.update_timer = None
        self.initialized = False
        # Delay initialization until screen is actually shown
        self.bind(on_enter=self.ensure_initialized)
    
    def ensure_initialized(self, *args):
        """Ensure the screen is initialized only when it's actually shown"""
        if not self.initialized:
            Clock.schedule_once(self.on_screen_init, 0)
            self.initialized = True
    
    def on_screen_init(self, dt):
        """Initialize screen after kivy has processed it"""
        # Get app instance
        self.app = App.get_running_app()
        
        # Create layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Add header
        header = BoxLayout(size_hint=(1, 0.1))
        header.add_widget(Label(text="", size_hint=(0.2, 1)))  # Left spacer for alignment
        header.add_widget(Label(text="Spotify", font_size=24))
        header.add_widget(Label(text="", size_hint=(0.2, 1)))  # Right spacer for alignment
        
        # Add album art
        self.album_image = Image(source="", size_hint=(1, 0.5))
        
        # Add track info
        info_box = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.track_label = Label(text=self.track_name, font_size=24)
        self.artist_label = Label(text=self.artist_name, font_size=18)
        self.album_label = Label(text=self.album_name, font_size=16)
        info_box.add_widget(self.track_label)
        info_box.add_widget(self.artist_label)
        info_box.add_widget(self.album_label)
        
        # Add progress bar (simplified as a label for now)
        progress_box = BoxLayout(size_hint=(1, 0.1))
        self.progress_label = Label(text=self.progress_text)
        progress_box.add_widget(self.progress_label)
        
        # Add playback controls
        controls_box = BoxLayout(size_hint=(1, 0.1))
        
        prev_button = Button(text="⏮")
        prev_button.bind(on_press=self.previous_track)
        
        self.play_pause_button = Button(text="⏸")
        self.play_pause_button.bind(on_press=self.play_pause)
        
        next_button = Button(text="⏭")
        next_button.bind(on_press=self.next_track)
        
        controls_box.add_widget(prev_button)
        controls_box.add_widget(self.play_pause_button)
        controls_box.add_widget(next_button)
        
        # Add all sections to main layout
        layout.add_widget(header)
        layout.add_widget(self.album_image)
        layout.add_widget(info_box)
        layout.add_widget(progress_box)
        layout.add_widget(controls_box)
        
        # Add layout to screen
        self.add_widget(layout)
    
    def update_track_info(self, track_info):
        """Update track information display"""
        self.track_info = track_info
        
        if track_info:
            # Update track details
            self.track_name = track_info['name']
            self.track_label.text = self.track_name
            
            self.artist_name = track_info['artist']
            self.artist_label.text = self.artist_name
            
            self.album_name = track_info['album']
            self.album_label.text = self.album_name
            
            # Update album art
            if 'album_art_path' in track_info:
                self.album_art = track_info['album_art_path']
                self.album_image.source = self.album_art
            
            # Update progress
            self._update_progress()
            
            # Start progress timer
            if self.update_timer:
                self.update_timer.cancel()
            self.update_timer = Clock.schedule_interval(self._update_progress, 1)
        else:
            # Clear display
            self.track_name = "No Track Playing"
            self.track_label.text = self.track_name
            
            self.artist_name = "--"
            self.artist_label.text = self.artist_name
            
            self.album_name = "--"
            self.album_label.text = self.album_name
            
            self.album_art = ""
            self.album_image.source = self.album_art
            
            self.progress_text = "--:-- / --:--"
            self.progress_label.text = self.progress_text
            
            # Stop progress timer
            if self.update_timer:
                self.update_timer.cancel()
                self.update_timer = None
    
    def _update_progress(self, dt=None):
        """Update progress display"""
        if not self.track_info:
            return
        
        # Get current track from Spotify manager
        current_track = self.app.spotify_manager.get_current_track()
        
        if current_track:
            # Update progress
            progress_ms = current_track['progress_ms']
            duration_ms = current_track['duration_ms']
            
            # Format as MM:SS
            progress_sec = int(progress_ms / 1000)
            duration_sec = int(duration_ms / 1000)
            
            progress_min = progress_sec // 60
            progress_sec = progress_sec % 60
            
            duration_min = duration_sec // 60
            duration_sec = duration_sec % 60
            
            self.progress_text = f"{progress_min:02d}:{progress_sec:02d} / {duration_min:02d}:{duration_sec:02d}"
            self.progress_label.text = self.progress_text
            
            # Update progress value
            self.progress_value = progress_ms / duration_ms if duration_ms > 0 else 0
    
    def play_pause(self, instance):
        """Toggle play/pause"""
        if self.app and self.app.spotify_manager:
            self.app.spotify_manager.play_pause()
            
            # Toggle button text
            if self.play_pause_button.text == "⏸":
                self.play_pause_button.text = "▶"
            else:
                self.play_pause_button.text = "⏸"
    
    def next_track(self, instance):
        """Skip to next track"""
        if self.app and self.app.spotify_manager:
            self.app.spotify_manager.next_track()
    
    def previous_track(self, instance):
        """Go back to previous track"""
        if self.app and self.app.spotify_manager:
            self.app.spotify_manager.previous_track()
    
    def go_back(self, instance):
        """Go back to weather screen"""
        if self.app:
            self.app.sm.current = 'weather'
    
    def on_enter(self):
        """Called when screen is entered"""
        # Reset last touch time to prevent screensaver
        Window.last_touch_time = Clock.get_time()
    
    def on_leave(self):
        """Called when screen is exited"""
        # Stop progress timer
        if self.update_timer:
            self.update_timer.cancel()
            self.update_timer = None
