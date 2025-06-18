# Performance Optimization Guide

This guide provides techniques to optimize the Smart Display application for the Raspberry Pi Zero 2W's limited resources.

## Hardware Considerations

### Memory Constraints

The Raspberry Pi Zero 2W has only 512MB of RAM, which can be a limiting factor:

- Monitor memory usage with `free -h` and `top`
- Consider adding a swap file if needed:

  ```bash
  sudo fallocate -l 1G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  ```

- Add to `/etc/fstab` for persistence:

  ```swapfile
  /swapfile swap swap defaults 0 0
  ```

### CPU Optimization

- Enable CPU governor for better performance:

  ```bash
  sudo apt install -y cpufrequtils
  sudo cpufreq-set -g performance
  ```

- Monitor CPU temperature: `vcgencmd measure_temp`
- Add heatsinks to prevent thermal throttling

### Storage Optimization

- Use Class 10 or higher microSD cards
- Consider enabling overlayfs to reduce SD card wear:

  ```bash
  sudo raspi-config
  # Advanced Options > Overlay FS > Enable
  ```

## Application Optimizations

### Image Handling

The photo slideshow can be memory-intensive:

- Resize images to match display resolution (1024×600)
- Limit the number of cached photos (default: 20)
- Use progressive JPEG loading
- Implement memory-efficient image rotation

```python
# Example of efficient image loading in Kivy
from kivy.core.image import Image as CoreImage
from io import BytesIO
from PIL import Image

def load_optimized_image(path, target_size=(1024, 600)):
    # Use PIL to resize efficiently
    with Image.open(path) as img:
        img = img.resize(target_size, Image.LANCZOS)
        
        # Convert to bytes for Kivy
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)
        
        # Create Kivy texture
        return CoreImage(buffer, ext='jpg').texture
```

### Background Services

Optimize background service behavior:

- Adjust update frequencies based on importance:
  - Weather updates: Every 30-60 minutes
  - Sensor readings: Every 1-5 minutes
  - Photo sync: Once per day or on demand
- Implement progressive backoff for network operations
- Use lazy initialization for non-critical components

### Network Optimization

- Cache network responses when appropriate
- Implement connection pooling
- Use compressed data formats when possible
- Implement retry mechanisms with exponential backoff

```python
# Example of network request with retry
import requests
import time

def fetch_with_retry(url, max_retries=3, backoff_factor=1.5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError):
            wait_time = backoff_factor ** retries
            time.sleep(wait_time)
            retries += 1
    
    # If all retries fail
    return None
```

### UI Performance

- Use Kivy's Atlas texture for grouping small images
- Implement screen caching to avoid rebuilding UI elements
- Use opacity for hiding/showing elements instead of removing/adding
- Limit animations and transitions
- Use Kivy's RecycleView instead of ListView for long lists

```python
# Example of efficient UI updates
from kivy.clock import Clock

def schedule_ui_update(self, data):
    # Schedule UI updates to avoid blocking the main thread
    Clock.schedule_once(lambda dt: self._update_ui(data), 0)
```

### Memory Management

- Implement proper cleanup when switching screens
- Use weakref for event callbacks
- Explicitly release resources when no longer needed
- Monitor memory leaks with tools like `memory_profiler`

## Testing and Profiling

### Performance Testing

- Use `cProfile` to identify bottlenecks:

  ```python
  import cProfile
  
  cProfile.run('app.run()', 'app_profile')
  ```

- Analyze results:

  ```bash
  python -m pstats app_profile
  ```

### Memory Profiling

- Install memory_profiler:

  ```bash
  pip install memory_profiler
  ```

- Profile memory usage:

  ```python
  from memory_profiler import profile
  
  @profile
  def memory_intensive_function():
      # Your code here
      pass
  ```

## System-Level Optimizations

### Disable Unnecessary Services

```bash
# List running services
systemctl list-units --type=service --state=running

# Disable unnecessary services
sudo systemctl disable bluetooth.service
sudo systemctl disable avahi-daemon.service
sudo systemctl disable triggerhappy.service
```

### Graphics Acceleration

- Enable OpenGL driver for better graphics performance:

  ```bash
  sudo raspi-config
  # Advanced Options > GL Driver > GL (Fake KMS)
  ```

### Boot Optimization

- Disable boot splash screen:

  ```bash
  sudo nano /boot/config.txt
  # Add: disable_splash=1
  ```

- Reduce boot services:

  ```bash
  sudo systemctl disable dhcpcd.service
  sudo systemctl disable keyboard-setup.service
  ```

## Monitoring Tools

- `htop`: Interactive process viewer
- `iotop`: Monitor disk I/O
- `vcgencmd`: Monitor GPU and CPU temperature
- `nethogs`: Monitor network usage per process

## Conclusion

By applying these optimizations, you can significantly improve the performance of the Smart Display application on the Raspberry Pi Zero 2W. Focus on reducing memory usage, efficient image handling, and optimizing network operations for the best results.
