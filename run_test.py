#!/usr/bin/env python3
"""
Test script to run the Smart Display application with mock data
This is a wrapper around the modular test structure in the tests/ package
"""
import os
import sys

# Import from tests package
from tests.asset_setup import create_mock_assets
from tests.mock_managers import (
    MockWiFiManager,
    MockLocationManager,
    MockWeatherManager,
    MockSensorManager,
    MockSpotifyManager,
    MockPhotoManager
)
from tests.ui_launcher import setup_environment, monkey_patch_managers, run_app

if __name__ == "__main__":
    print("Smart Display Test Launcher")
    print("==========================")
    
    # Setup test environment
    setup_environment()
    
    # Patch manager classes
    monkey_patch_managers()
    
    # Run application
    run_app()
