# Smart Display Usage Guide

This guide explains how to use the various features of your Smart Display.

## Navigation

The Smart Display has four main screens:

1. **Weather Screen** - Displays weather information and indoor sensor data
2. **Photos Screen** - Shows photo slideshow
3. **Spotify Screen** - Controls Spotify playback
4. **Settings Screen** - Configure device settings

Navigate between screens using the navigation bar at the bottom of the display.

## Weather Screen

The Weather Screen displays:

- Current temperature, conditions, and weather icon
- Hourly forecast for the next 24 hours
- Daily forecast for the next 7 days
- Indoor temperature, humidity, pressure, and air quality from the BME680 sensor

The weather data automatically updates every 30 minutes.

## Photos Screen

The Photos Screen displays photos from your configured Google Photos album as a slideshow.

- Photos automatically transition based on your configured interval (default: 30 seconds)
- Tap anywhere on the screen to manually advance to the next photo
- Photos are cached locally for offline viewing

## Spotify Screen

The Spotify Screen allows you to control Spotify playback:

- Play/Pause button toggles playback
- Next/Previous buttons change tracks
- Album art and track information is displayed
- Volume can be adjusted using the slider

Your Smart Display acts as a Spotify Connect device, allowing you to select it as a playback device from any Spotify app.

## Settings Screen

The Settings Screen is organized into tabs:

### Display Settings

- **Brightness**: Adjust screen brightness
- **Timeout**: Set screen timeout duration
- **Clock Format**: Choose 12-hour or 24-hour format

### WiFi Settings

- **Scan**: Scan for available WiFi networks
- **Connect**: Connect to a selected network
- **Manual Entry**: Connect to a hidden network

### API Keys

- View and update API keys for:
  - OpenWeatherMap
  - Google Geolocation
  - Spotify

### Spotify Settings

- **Device Name**: Change the Spotify Connect device name
- **Quality**: Adjust audio quality settings

### System Settings

- **Restart App**: Restart the Smart Display application
- **Reboot**: Reboot the Raspberry Pi
- **Shutdown**: Safely shut down the Raspberry Pi

## Touch Gestures

- **Tap**: Select an item or button
- **Swipe Left/Right**: On some screens, navigate between panels
- **Swipe Down**: On the Weather Screen, refresh weather data

## On-Screen Keyboard

When you need to enter text (e.g., WiFi password, API key):

1. Tap on the text field
2. The on-screen keyboard will appear
3. Type your text
4. Press Enter or tap outside the keyboard to dismiss it

## Automatic Features

- **Weather Updates**: Weather data updates automatically every 30 minutes
- **Sensor Readings**: Indoor sensor data updates every minute
- **Photo Sync**: Photos sync from Google Photos daily
- **WiFi Reconnection**: Automatically reconnects to known networks
