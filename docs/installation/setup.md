# Smart Display Installation Guide

This guide provides step-by-step instructions for setting up the Smart Display application on a Raspberry Pi Zero 2W.

## Prerequisites

Before beginning installation, ensure you have:

- Raspberry Pi Zero 2W with Raspberry Pi OS (Bullseye or newer) installed
- 7" Waveshare touchscreen connected and working
- BME680 sensor
- Internet connection
- Required API keys (see [API Setup](../api/keys.md))

## Basic Setup

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
# Install system dependencies
sudo apt install -y python3-pip python3-venv git i2c-tools libjpeg-dev zlib1g-dev libffi-dev libssl-dev

# Enable I2C interface for the BME680 sensor
sudo raspi-config nonint do_i2c 0

# Install NetworkManager for WiFi management
sudo apt install -y network-manager network-manager-gnome
```

### 3. Create Installation Directory

```bash
sudo mkdir -p /opt/smartdisplay
sudo chown pi:pi /opt/smartdisplay
```

### 4. Clone Repository

```bash
git clone https://github.com/yourusername/pi_smart_display.git /opt/smartdisplay
cd /opt/smartdisplay
```

### 5. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 6. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Sensor Setup

### 1. Connect BME680 Sensor

Connect the BME680 sensor to the Raspberry Pi's I2C pins:

- VCC to 3.3V (Pin 1)
- GND to Ground (Pin 6)
- SCL to I2C Clock (Pin 5)
- SDA to I2C Data (Pin 3)

### 2. Verify Sensor Connection

```bash
# Check if the sensor is detected
i2cdetect -y 1
```

You should see the BME680 sensor address (typically 0x76 or 0x77) in the output.

## API Configuration

### 1. Create Environment File

```bash
cp .env.example .env
nano .env
```

### 2. Add API Keys

Add your API keys to the .env file:

```weathermap
OPENWEATHERMAP_API_KEY=your_api_key_here
GOOGLE_GEOLOCATION_API_KEY=your_api_key_here
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

See [API Setup](../api/keys.md) for instructions on obtaining these keys.

## Spotify Integration

### 1. Install Librespot

```bash
# Install Rust (required for librespot)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Clone and build librespot
git clone https://github.com/librespot-org/librespot.git
cd librespot
cargo build --release --features="alsa-backend"
sudo cp target/release/librespot /usr/local/bin/
```

### 2. Configure Librespot Service

```bash
sudo nano /etc/systemd/system/librespot.service
```

Add the following content:

```spotify
[Unit]
Description=Librespot Spotify Connect
After=network.target

[Service]
ExecStart=/usr/local/bin/librespot --name "Smart Display" --backend alsa --device default --bitrate 320
Restart=always
RestartSec=10
User=pi

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable librespot
sudo systemctl start librespot
```

## Autostart Configuration

### 1. Create Systemd Service

```bash
sudo nano /etc/systemd/system/smartdisplay.service
```

Add the following content:

```display
[Unit]
Description=Smart Display Application
After=network.target

[Service]
ExecStart=/opt/smartdisplay/venv/bin/python /opt/smartdisplay/main.py
WorkingDirectory=/opt/smartdisplay
Restart=always
RestartSec=10
User=pi

[Install]
WantedBy=multi-user.target
```

### 2. Enable and Start Service

```bash
sudo systemctl enable smartdisplay
sudo systemctl start smartdisplay
```

## Display Configuration

### 1. Configure Display Resolution

Edit the config.txt file:

```bash
sudo nano /boot/config.txt
```

Add/modify these lines:

```hdmi
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1024 600 60 6 0 0 0
hdmi_drive=1
```

### 2. Disable Screen Blanking

```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

Add these lines:

```xset
@xset s off
@xset -dpms
@xset s noblank
```

## Testing the Installation

### 1. Manual Test

```bash
cd /opt/smartdisplay
source venv/bin/activate
python main.py
```

### 2. Service Test

```bash
sudo systemctl status smartdisplay
```

## Troubleshooting

If you encounter issues:

1. Check logs: `sudo journalctl -u smartdisplay -f`
2. Verify sensor connection: `i2cdetect -y 1`
3. Test network connectivity: `ping -c 4 google.com`
4. Verify API keys in .env file
5. Check permissions: `ls -la /opt/smartdisplay`

For more detailed troubleshooting, see [Troubleshooting Guide](../usage/troubleshooting.md).
