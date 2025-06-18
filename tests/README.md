# Smart Display Test Suite

This directory contains the modular test suite for the Smart Display application.

## Overview

The test suite is organized into several modules:

- `asset_setup.py` - Creates mock assets for testing (weather icons, photos, etc.)
- `mock_managers.py` - Provides mock implementations of all manager classes
- `ui_launcher.py` - Main entry point for running the UI tests

## Running Tests

To run the tests, use the wrapper script in the project root:

```bash
python run_test.py
```

This will:
1. Set up the test environment (create .env file, directories, etc.)
2. Create mock assets for testing
3. Patch manager classes with mock implementations
4. Launch the application UI

## Test Environment

The test environment simulates:

- WiFi connectivity and network scanning
- Location services (fixed to New York City)
- Weather data from OpenWeatherMap
- Sensor readings from BME680
- Spotify integration
- Photo management and slideshows

## Customizing Tests

To customize the test behavior:

1. Modify mock implementations in `mock_managers.py`
2. Adjust asset generation in `asset_setup.py`
3. Configure UI settings in `ui_launcher.py`

## Adding New Tests

To add new test components:

1. Create a new module in the `tests/` directory
2. Import and use it in `ui_launcher.py`
3. Update this README with documentation

## Troubleshooting

If you encounter issues:

- Check that all dependencies are installed
- Verify the .env file has been created with mock API keys
- Ensure mock assets have been generated properly
- Check console output for error messages
