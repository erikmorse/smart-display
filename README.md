# Smart Display

![CI](https://github.com/yourusername/smart-display/workflows/CI/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)

A Raspberry Pi-based smart display application showing weather, photos, and Spotify controls.

## Overview

This project turns a Raspberry Pi Zero 2W with a touchscreen into a smart display that shows:

- Weather information (current conditions and forecast)
- Indoor environment data from BME680 sensor (temperature, humidity, pressure, air quality)
- Photo slideshow from Google Photos
- Spotify controls and now playing information

The application is built with Python and Kivy for a responsive touch interface.

## Quick Start

### Prerequisites

- Raspberry Pi Zero 2W (or newer)
- 7" Touchscreen display (Waveshare 1024×600 recommended)
- BME680 environmental sensor
- Raspbian OS (Bullseye or newer)
- Python 3.9+

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/smart-display.git
   cd smart-display
   ```

2. Install dependencies:

   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   sudo apt install -y libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good
   sudo apt install -y network-manager i2c-tools
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   nano .env  # Add your API keys and settings
   ```

4. Set up autostart:

   ```bash
   sudo cp smartdisplay.service /etc/systemd/system/
   sudo systemctl enable smartdisplay
   sudo systemctl start smartdisplay
   ```

For detailed installation instructions, see the [complete installation guide](docs/installation/setup.md).

## Documentation

See the [docs](docs/) directory for complete documentation, including:

- [Hardware requirements](docs/hardware/requirements.md)
- [Installation guide](docs/installation/setup.md)
- [Usage instructions](docs/usage/overview.md)
- [Development notes](docs/development/overview.md)
- [API documentation](docs/api/overview.md)
- [Troubleshooting](docs/usage/troubleshooting.md)
- [Performance optimization](docs/development/performance.md)

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-display.git
cd smart-display

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests

# Run the application in development mode
python run_test.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
