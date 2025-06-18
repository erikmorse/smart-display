"""
Asset setup module for Smart Display tests
Creates mock assets for testing the application
"""
import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFont

def create_mock_assets():
    """Create mock assets for testing"""
    print("Creating mock assets for testing...")
    
    # Create directories if they don't exist
    directories = [
        'assets',
        'assets/icons',
        'assets/weather_icons',
        'assets/photos'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
    
    # Create mock weather icons
    weather_icons = [
        '01d.png', '01n.png',  # clear sky
        '02d.png', '02n.png',  # few clouds
        '03d.png', '03n.png',  # scattered clouds
        '04d.png', '04n.png',  # broken clouds
        '09d.png', '09n.png',  # shower rain
        '10d.png', '10n.png',  # rain
        '11d.png', '11n.png',  # thunderstorm
        '13d.png', '13n.png',  # snow
        '50d.png', '50n.png',  # mist
    ]
    
    for icon in weather_icons:
        icon_path = f'assets/weather_icons/{icon}'
        if not os.path.exists(icon_path):
            create_mock_icon(icon_path, icon[:-4])
            print(f"Created mock weather icon: {icon}")
    
    # Create mock photos for slideshow
    for i in range(5):
        photo_path = f'assets/photos/photo_{i}.jpg'
        if not os.path.exists(photo_path):
            create_mock_photo(photo_path, f'Photo {i}')
            print(f"Created mock photo: photo_{i}.jpg")
    
    # Create mock album art for Spotify
    album_path = 'assets/icons/album.jpg'
    if not os.path.exists(album_path):
        create_mock_album(album_path)
        print("Created mock album art")
    
    print("Mock assets created successfully!")

def create_mock_icon(path, text):
    """Create a mock weather icon"""
    img = Image.new('RGBA', (100, 100), color=(73, 109, 137, 255))
    d = ImageDraw.Draw(img)
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    d.text((10, 40), text, fill=(255, 255, 255), font=font)
    img.save(path)

def create_mock_photo(path, text):
    """Create a mock photo for slideshow"""
    # Random color for the photo
    r = random.randint(0, 200)
    g = random.randint(0, 200)
    b = random.randint(0, 200)
    
    img = Image.new('RGB', (800, 600), color=(r, g, b))
    d = ImageDraw.Draw(img)
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    d.text((300, 280), text, fill=(255, 255, 255), font=font)
    img.save(path)

def create_mock_album(path):
    """Create a mock album art for Spotify"""
    img = Image.new('RGB', (300, 300), color=(30, 215, 96))  # Spotify green
    d = ImageDraw.Draw(img)
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
    
    d.text((80, 140), "Mock Album", fill=(255, 255, 255), font=font)
    img.save(path)

if __name__ == "__main__":
    create_mock_assets()
