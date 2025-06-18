"""
Spotify Manager Module for Smart Display
Handles Spotify integration and playback control
"""
import os
import json
import time
import subprocess
import threading
from datetime import datetime
import requests
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

# Load environment variables
load_dotenv()

class SpotifyManager:
    """Manages Spotify integration and playback control"""
    
    def __init__(self, status_callback=None):
        """Initialize Spotify Manager"""
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'config', 'spotify.json')
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'assets', 'album_art')
        self.status_callback = status_callback
        self.sp = None
        self.current_track = None
        self.is_playing = False
        self.librespot_process = None
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize Spotify API client
        self._init_spotify_api()
        
        # Start librespot in a separate thread
        threading.Thread(target=self._start_librespot, daemon=True).start()
        
        # Start polling for playback status
        threading.Thread(target=self._poll_playback_status, daemon=True).start()
    
    def _init_spotify_api(self):
        """Initialize Spotify API client with mock data for testing"""
        # For testing purposes, we'll use mock data instead of authenticating
        print("Using mock Spotify data for testing")
        
        # Create a mock track
        self.current_track = {
            'id': 'mock_track_id',
            'name': 'Mock Song Title',
            'artist': 'Mock Artist',
            'album': 'Mock Album',
            'album_art': None,
            'album_art_path': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                         'assets', 'album_art', 'mock_album.jpg'),
            'duration_ms': 180000,
            'progress_ms': 45000
        }
        
        # Create mock album art if it doesn't exist
        album_art_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'album_art')
        os.makedirs(album_art_dir, exist_ok=True)
        
        album_art_path = os.path.join(album_art_dir, 'mock_album.jpg')
        if not os.path.exists(album_art_path):
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (300, 300), color=(20, 20, 20))
                draw = ImageDraw.Draw(img)
                draw.ellipse([(50, 50), (250, 250)], fill=(30, 215, 96))  # Spotify green
                img.save(album_art_path)
            except Exception as e:
                print(f"Error creating mock album art: {e}")
        
        self.is_playing = True
        
        # We'll delay the callback until start_monitoring is called
        # This ensures the app is fully initialized before we try to access screens
        
        return True
    
    def _start_librespot(self):
        """Mock librespot for Spotify Connect functionality"""
        print("Using mock Spotify Connect functionality for testing")
        # We don't actually start librespot in test mode
        # This avoids the need for Spotify credentials
    
    def _poll_playback_status(self):
        """Mock polling for playback status changes"""
        print("Using mock Spotify playback status for testing")
        
        # In test mode, we just simulate a playing track
        # No need to poll Spotify API
        
        # Sleep to avoid CPU usage
        time.sleep(5)
        
        # We've already set up the mock track in _init_spotify_api
        # and called the status callback there, so nothing more to do here
    
    def _download_album_art(self, url, track_id):
        """Download album art and resize it"""
        try:
            # Check if we already have this album art
            file_path = os.path.join(self.cache_dir, f"{track_id}.jpg")
            
            if os.path.exists(file_path):
                return file_path
            
            # Download the image
            response = requests.get(url)
            
            if response.status_code == 200:
                # Save the original image
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                # Resize the image to a reasonable size for the display
                img = Image.open(file_path)
                img = img.resize((300, 300), Image.LANCZOS)
                img.save(file_path)
                
                return file_path
            
            return None
            
        except Exception as e:
            print(f"Error downloading album art: {e}")
            return None
    
    def play_pause(self):
        """Toggle play/pause"""
        if not self.sp:
            print("Spotify API client not initialized")
            return False
        
        try:
            if self.is_playing:
                self.sp.pause_playback()
            else:
                self.sp.start_playback()
            
            return True
            
        except Exception as e:
            print(f"Error toggling play/pause: {e}")
            return False
    
    def next_track(self):
        """Skip to next track"""
        if not self.sp:
            print("Spotify API client not initialized")
            return False
        
        try:
            self.sp.next_track()
            return True
            
        except Exception as e:
            print(f"Error skipping to next track: {e}")
            return False
    
    def previous_track(self):
        """Go back to previous track"""
        if not self.sp:
            print("Spotify API client not initialized")
            return False
        
        try:
            self.sp.previous_track()
            return True
            
        except Exception as e:
            print(f"Error going to previous track: {e}")
            return False
    
    def get_current_track(self):
        """Get current track information"""
        return self.current_track
    
    def start_monitoring(self):
        """Start monitoring Spotify playback status"""
        print("Starting Spotify monitoring...")
        # This is already handled in __init__ through _poll_playback_status
        # This method exists for compatibility with main.py
        
        # Add a delay before triggering the callback to ensure the app is fully initialized
        def delayed_callback():
            # Wait 3 seconds to ensure app is fully initialized
            time.sleep(3)
            # Then trigger the callback if it exists
            if self.status_callback and self.current_track:
                print("Triggering delayed Spotify status callback")
                self.status_callback(True, self.current_track)
        
        # Start the delayed callback in a separate thread
        threading.Thread(target=delayed_callback, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop monitoring Spotify playback status"""
        print("Stopping Spotify monitoring...")
        # Clean up resources
        if self.librespot_process:
            try:
                self.librespot_process.terminate()
            except Exception as e:
                print(f"Error stopping librespot: {e}")
        
        # Set flags to stop polling threads
        self.is_playing = False
        self.current_track = None
