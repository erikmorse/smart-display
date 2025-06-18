"""
Photo Manager Module for Smart Display
Handles photo syncing and slideshow functionality
"""
import os
import json
import random
import subprocess
import threading
import time
from datetime import datetime
from PIL import Image

class PhotoManager:
    """Manages photo syncing and slideshow functionality"""
    
    def __init__(self):
        """Initialize Photo Manager"""
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                       'config', 'photos.json')
        self.photos_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'assets', 'photos')
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'assets', 'photos_cache')
        self.config = self.load_config()
        self.photo_list = []
        self.current_photo_index = 0
        self.last_sync = None
        
        # Create directories if they don't exist
        os.makedirs(self.photos_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load photo list
        self.load_photo_list()
        
        # Start sync thread
        threading.Thread(target=self._sync_photos_thread, daemon=True).start()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'album_id': '',
            'sync_interval': 3600,  # 1 hour
            'slideshow_interval': 30,  # 30 seconds
            'last_sync': None
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Error loading photo config: {e}")
                return default_config
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Save to file
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)
    
    def load_photo_list(self):
        """Load list of available photos"""
        self.photo_list = []
        
        # Check photos directory
        if os.path.exists(self.photos_dir):
            for filename in os.listdir(self.photos_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.photo_list.append(os.path.join(self.photos_dir, filename))
        
        # If no photos found, use sample images
        if not self.photo_list:
            print("No photos found, using sample images")
            sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'assets', 'sample_photos')
            
            # Create sample directory if it doesn't exist
            os.makedirs(sample_dir, exist_ok=True)
            
            # Create a sample image if none exist
            if not os.listdir(sample_dir):
                self._create_sample_image(sample_dir)
            
            # Add sample images to list
            for filename in os.listdir(sample_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.photo_list.append(os.path.join(sample_dir, filename))
        
        # Shuffle the list
        random.shuffle(self.photo_list)
    
    def _create_sample_image(self, directory):
        """Create a sample image"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a blank image
            img = Image.new('RGB', (1024, 600), color=(73, 109, 137))
            
            # Get a drawing context
            d = ImageDraw.Draw(img)
            
            # Draw text
            d.text((10, 10), "Smart Display", fill=(255, 255, 0))
            d.text((10, 50), "Sample Image", fill=(255, 255, 0))
            d.text((10, 90), "Please configure Google Photos", fill=(255, 255, 0))
            
            # Save the image
            img.save(os.path.join(directory, 'sample.jpg'))
            
        except Exception as e:
            print(f"Error creating sample image: {e}")
    
    def _sync_photos_thread(self):
        """Thread to periodically sync photos"""
        while True:
            # Check if sync is needed
            if self.config['album_id']:
                current_time = time.time()
                last_sync = self.config.get('last_sync', 0)
                
                if not last_sync or (current_time - last_sync) > self.config['sync_interval']:
                    self.sync_photos()
            
            # Sleep for a while
            time.sleep(300)  # Check every 5 minutes
    
    def sync_photos(self):
        """Sync photos from Google Photos"""
        if not self.config['album_id']:
            print("No album ID configured")
            return False
        
        try:
            # Check if gphotos-sync is installed
            result = subprocess.run(['which', 'gphotos-sync'], capture_output=True, text=True)
            
            if result.returncode != 0:
                print("gphotos-sync not found. Please install it for Google Photos integration.")
                return False
            
            # Run gphotos-sync to download photos
            cmd = [
                'gphotos-sync',
                '--album', self.config['album_id'],
                '--resync',
                self.photos_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Photos synced successfully")
                
                # Update last sync time
                self.config['last_sync'] = time.time()
                self.save_config()
                
                # Reload photo list
                self.load_photo_list()
                
                # Process photos for display
                self._process_photos()
                
                return True
            else:
                print(f"Error syncing photos: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error syncing photos: {e}")
            return False
    
    def _process_photos(self):
        """Process photos for display (resize, etc.)"""
        # Clear cache directory
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        
        # Process each photo
        for i, photo_path in enumerate(self.photo_list):
            try:
                # Open the image
                img = Image.open(photo_path)
                
                # Calculate new size while maintaining aspect ratio
                width, height = img.size
                ratio = min(1024 / width, 600 / height)
                new_size = (int(width * ratio), int(height * ratio))
                
                # Resize the image
                img = img.resize(new_size, Image.LANCZOS)
                
                # Create a new image with black background
                new_img = Image.new('RGB', (1024, 600), (0, 0, 0))
                
                # Paste the resized image in the center
                x = (1024 - new_size[0]) // 2
                y = (600 - new_size[1]) // 2
                new_img.paste(img, (x, y))
                
                # Save to cache
                cache_path = os.path.join(self.cache_dir, f"photo_{i}.jpg")
                new_img.save(cache_path, quality=85)
                
            except Exception as e:
                print(f"Error processing photo {photo_path}: {e}")
    
    def get_next_photo(self):
        """Get the next photo for slideshow"""
        if not self.photo_list:
            return None
        
        # Get the next photo
        photo = self.photo_list[self.current_photo_index]
        
        # Increment index
        self.current_photo_index = (self.current_photo_index + 1) % len(self.photo_list)
        
        # Check if we have a cached version
        cache_path = os.path.join(self.cache_dir, f"photo_{self.current_photo_index}.jpg")
        if os.path.exists(cache_path):
            return cache_path
        
        return photo
    
    def set_album_id(self, album_id):
        """Set the Google Photos album ID"""
        self.config['album_id'] = album_id
        self.save_config()
        
        # Trigger a sync
        threading.Thread(target=self.sync_photos, daemon=True).start()
    
    def set_slideshow_interval(self, interval):
        """Set the slideshow interval in seconds"""
        self.config['slideshow_interval'] = interval
        self.save_config()
    
    def get_slideshow_interval(self):
        """Get the slideshow interval in seconds"""
        return self.config['slideshow_interval']
    
    def stop_sync(self):
        """Stop photo syncing"""
        print("Stopping photo sync...")
        # This is a placeholder method for compatibility with main.py
        # In a real implementation, this would stop any running sync processes
        pass
