# Hardware Requirements

This document outlines the hardware requirements for the Smart Display project.

## Core Components

| Component | Specification | Notes |
|-----------|---------------|-------|
| Single-Board Computer | Raspberry Pi Zero 2W | 1GHz quad-core ARM Cortex-A53 CPU, 512MB RAM |
| Display | Waveshare 7" Touchscreen | 1024×600 resolution, 5-point capacitive touch |
| Environmental Sensor | BME680 | Temperature, humidity, pressure, and VOC sensor |
| Storage | MicroSD Card (16GB+ recommended) | Class 10 or higher for better performance |
| Power Supply | 5V/2.5A USB-C Power Adapter | Ensure stable power for both Pi and display |
| Case | Optional but recommended | Protects components and improves appearance |

## Display Connection

The Waveshare 7" touchscreen connects to the Raspberry Pi Zero 2W via:

- HDMI connection for video (using mini-HDMI adapter)
- USB connection for touch functionality (using OTG adapter)

## Sensor Connection

The BME680 sensor connects to the Raspberry Pi via I²C:

| BME680 Pin | Raspberry Pi Pin |
|------------|------------------|
| VCC | 3.3V (Pin 1) |
| GND | Ground (Pin 6) |
| SCL | I²C Clock (Pin 5) |
| SDA | I²C Data (Pin 3) |

## Optional Components

- **USB Speaker/Headphones**: For Spotify audio output
- **USB WiFi Adapter**: If stronger WiFi reception is needed
- **GPIO Buttons**: For physical controls (optional)

## Power Considerations

The Raspberry Pi Zero 2W with the 7" display and BME680 sensor draws approximately:

- Idle: ~350mA (1.75W)
- Average usage: ~450mA (2.25W)
- Peak usage: ~600mA (3W)

Ensure your power supply can provide at least 2.5A to avoid undervoltage issues.

## Performance Considerations

The Raspberry Pi Zero 2W has limited resources:

- 1GHz quad-core CPU
- 512MB RAM

This is sufficient for the Smart Display application, but be aware of these limitations when adding additional features or running other applications simultaneously.

## Compatible Alternatives

If the Raspberry Pi Zero 2W is unavailable or insufficient for your needs, these alternatives are compatible:

- Raspberry Pi 3B/3B+/4B (more powerful, higher power consumption)
- Raspberry Pi Zero W (less powerful, may have performance issues with some features)

For the display, any HDMI-compatible touchscreen should work, but the UI is optimized for the 7" 1024×600 resolution.
