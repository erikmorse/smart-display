# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Smart Display.

## Startup Issues

### Display Shows Black Screen

**Possible causes:**

- Power supply insufficient
- HDMI connection issue
- Application crash

**Solutions:**

1. Check power supply (use 5V/2.5A or higher)
2. Verify HDMI connections
3. Check application logs: `sudo journalctl -u smartdisplay -f`
4. Restart the application: `sudo systemctl restart smartdisplay`

### Application Crashes on Startup

**Possible causes:**

- Missing dependencies
- Incorrect permissions
- API configuration issues

**Solutions:**

1. Check logs: `sudo journalctl -u smartdisplay -f`
2. Verify all dependencies are installed: `pip list`
3. Check file permissions: `ls -la /opt/smartdisplay`
4. Verify .env file exists and contains valid API keys

## Weather Issues

### Weather Data Not Displaying

**Possible causes:**

- No internet connection
- Invalid API key
- Location services issue

**Solutions:**

1. Check internet connection: `ping -c 4 google.com`
2. Verify OpenWeatherMap API key in .env file
3. Check location settings in the application
4. Manually refresh weather data by swiping down on the Weather Screen

### Indoor Sensor Data Missing

**Possible causes:**

- BME680 sensor not connected properly
- I2C not enabled
- Sensor driver issue

**Solutions:**

1. Check sensor connections
2. Verify I2C is enabled: `sudo raspi-config`
3. Check if sensor is detected: `i2cdetect -y 1`
4. Restart the application: `sudo systemctl restart smartdisplay`

## WiFi Issues

### Cannot Connect to WiFi

**Possible causes:**

- Incorrect password
- Network out of range
- NetworkManager issues

**Solutions:**

1. Verify password is correct
2. Check signal strength
3. Restart NetworkManager: `sudo systemctl restart NetworkManager`
4. Try connecting to a different network

### WiFi Disconnects Frequently

**Possible causes:**

- Weak signal
- Power management settings
- Router issues

**Solutions:**

1. Move closer to the router
2. Disable WiFi power management:

   ```bash
   sudo nano /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
   # Set wifi.powersave = 2
   ```

3. Restart NetworkManager: `sudo systemctl restart NetworkManager`

## Spotify Issues

### Spotify Connect Device Not Appearing

**Possible causes:**

- Librespot service not running
- Network issues
- Spotify account problems

**Solutions:**

1. Check librespot service: `sudo systemctl status librespot`
2. Restart librespot: `sudo systemctl restart librespot`
3. Verify network connectivity
4. Check Spotify credentials in .env file

### No Sound from Spotify

**Possible causes:**

- Volume too low
- Audio output configuration issue
- ALSA problems

**Solutions:**

1. Check volume settings in Spotify app
2. Verify audio output device: `aplay -l`
3. Test audio: `aplay /usr/share/sounds/alsa/Front_Center.wav`
4. Restart librespot: `sudo systemctl restart librespot`

## Photo Issues

### Photos Not Displaying

**Possible causes:**

- No photos synced
- Incorrect album configuration
- Storage issues

**Solutions:**

1. Check if photos are synced: `ls -la /opt/smartdisplay/assets/photos`
2. Verify Google Photos configuration
3. Check available storage: `df -h`
4. Manually trigger photo sync (via Settings)

### Photo Slideshow Too Fast/Slow

**Solution:**

- Adjust slideshow interval in Settings > Display

## Touch Screen Issues

### Touch Not Responding

**Possible causes:**

- USB connection issue
- Driver problem
- Calibration issue

**Solutions:**

1. Check USB connections
2. Restart the device: `sudo reboot`
3. Recalibrate touchscreen:

   ```bash
   sudo apt install -y xinput-calibrator
   xinput_calibrator
   ```

### On-Screen Keyboard Not Appearing

**Possible causes:**

- Kivy configuration issue
- Input method problem

**Solutions:**

1. Restart the application: `sudo systemctl restart smartdisplay`
2. Check Kivy configuration: `~/.kivy/config.ini`

## Performance Issues

### Application Running Slowly

**Possible causes:**

- Too many background processes
- Limited RAM
- CPU throttling due to overheating

**Solutions:**

1. Check running processes: `top`
2. Check temperature: `vcgencmd measure_temp`
3. Add a heatsink to the Raspberry Pi
4. Optimize application settings (reduce photo quality, increase update intervals)

## System Issues

### High CPU/Memory Usage

**Solutions:**

1. Check resource usage: `top`
2. Identify resource-intensive processes
3. Adjust update frequencies in Settings
4. Restart the application: `sudo systemctl restart smartdisplay`

### Device Overheating

**Solutions:**

1. Check temperature: `vcgencmd measure_temp`
2. Improve ventilation
3. Add a heatsink
4. Reduce screen brightness

## Getting Support

If you're still experiencing issues:

1. Check the full documentation at [docs/README.md](../README.md)
2. Look for similar issues in the project repository
3. Collect logs for troubleshooting:

   ```bash
   sudo journalctl -u smartdisplay -n 100 > smartdisplay-logs.txt
   sudo journalctl -u librespot -n 100 > librespot-logs.txt
   ```
