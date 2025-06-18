"""
Weather Screen Module for Smart Display
Displays weather information and indoor environmental data
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.app import App
from datetime import datetime

class WeatherScreen(Screen):
    """Weather Screen for displaying weather and environmental data"""
    
    # Weather properties
    city_name = StringProperty("Loading...")
    current_temp = StringProperty("--°C")
    current_condition = StringProperty("--")
    current_humidity = StringProperty("--")
    current_wind = StringProperty("--")
    current_pressure = StringProperty("--")
    
    # Indoor sensor properties
    indoor_temp = StringProperty("--°C")
    indoor_humidity = StringProperty("--")
    indoor_pressure = StringProperty("--")
    indoor_air_quality = StringProperty("--")
    
    # Weather icon
    weather_icon = StringProperty("")
    
    def __init__(self, **kwargs):
        """Initialize Weather Screen"""
        super(WeatherScreen, self).__init__(**kwargs)
        self.app = None
        Clock.schedule_once(self.on_screen_init, 0)
    
    def on_screen_init(self, dt):
        """Initialize screen after kivy has processed it"""
        # Get app instance
        self.app = App.get_running_app()
        
        # Create layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add header with city name
        header = BoxLayout(size_hint=(1, 0.1))
        self.city_label = Label(text=self.city_name, font_size=24)
        header.add_widget(self.city_label)
        
        # Add main weather display
        weather_box = BoxLayout(size_hint=(1, 0.4))
        
        # Left side - current conditions
        left_box = BoxLayout(orientation='vertical')
        self.weather_image = Image(source="")
        self.temp_label = Label(text=self.current_temp, font_size=48)
        self.condition_label = Label(text=self.current_condition)
        left_box.add_widget(self.weather_image)
        left_box.add_widget(self.temp_label)
        left_box.add_widget(self.condition_label)
        
        # Right side - details
        right_box = GridLayout(cols=2)
        right_box.add_widget(Label(text="Humidity:"))
        self.humidity_label = Label(text=self.current_humidity)
        right_box.add_widget(self.humidity_label)
        
        right_box.add_widget(Label(text="Wind:"))
        self.wind_label = Label(text=self.current_wind)
        right_box.add_widget(self.wind_label)
        
        right_box.add_widget(Label(text="Pressure:"))
        self.pressure_label = Label(text=self.current_pressure)
        right_box.add_widget(self.pressure_label)
        
        weather_box.add_widget(left_box)
        weather_box.add_widget(right_box)
        
        # Add forecast
        forecast_box = BoxLayout(size_hint=(1, 0.3))
        self.forecast_widgets = []
        
        for i in range(5):
            day_box = BoxLayout(orientation='vertical')
            day_label = Label(text=f"Day {i+1}")
            day_image = Image(source="")
            day_temp = Label(text="--°C")
            
            day_box.add_widget(day_label)
            day_box.add_widget(day_image)
            day_box.add_widget(day_temp)
            
            forecast_box.add_widget(day_box)
            self.forecast_widgets.append((day_label, day_image, day_temp))
        
        # Add indoor sensor data
        sensor_box = BoxLayout(size_hint=(1, 0.2))
        sensor_box.add_widget(Label(text="Indoor Conditions", font_size=18))
        
        sensor_grid = GridLayout(cols=4)
        
        # Temperature
        temp_box = BoxLayout(orientation='vertical')
        temp_box.add_widget(Label(text="Temperature"))
        self.indoor_temp_label = Label(text=self.indoor_temp, font_size=20)
        temp_box.add_widget(self.indoor_temp_label)
        sensor_grid.add_widget(temp_box)
        
        # Humidity
        humidity_box = BoxLayout(orientation='vertical')
        humidity_box.add_widget(Label(text="Humidity"))
        self.indoor_humidity_label = Label(text=self.indoor_humidity, font_size=20)
        humidity_box.add_widget(self.indoor_humidity_label)
        sensor_grid.add_widget(humidity_box)
        
        # Pressure
        pressure_box = BoxLayout(orientation='vertical')
        pressure_box.add_widget(Label(text="Pressure"))
        self.indoor_pressure_label = Label(text=self.indoor_pressure, font_size=20)
        pressure_box.add_widget(self.indoor_pressure_label)
        sensor_grid.add_widget(pressure_box)
        
        # Air Quality
        air_box = BoxLayout(orientation='vertical')
        air_box.add_widget(Label(text="Air Quality"))
        self.indoor_air_label = Label(text=self.indoor_air_quality, font_size=20)
        air_box.add_widget(self.indoor_air_label)
        sensor_grid.add_widget(air_box)
        
        sensor_box.add_widget(sensor_grid)
        
        # Add all sections to main layout
        layout.add_widget(header)
        layout.add_widget(weather_box)
        layout.add_widget(forecast_box)
        layout.add_widget(sensor_box)
        
        # Add layout to screen
        self.add_widget(layout)
        
        # Schedule weather update
        Clock.schedule_once(self.update_weather, 1)
    
    def update_weather(self, dt):
        """Update weather display with data from weather manager"""
        if not self.app:
            return
        
        weather_data = self.app.weather_manager.get_weather_data()
        
        if weather_data:
            self.update_weather_display(weather_data)
    
    def update_weather_data(self, weather_data):
        """Update weather display with provided weather data (alias for compatibility with main.py)"""
        self.update_weather_display(weather_data)
    
    def update_weather_display(self, weather_data):
        """Update the weather display with the provided weather data"""
        if weather_data:
            # Update current weather
            current = weather_data['current']
            self.city_name = f"{current['city']}, {current['country']}"
            self.city_label.text = self.city_name
            
            self.current_temp = f"{current['temp']}°C"
            self.temp_label.text = self.current_temp
            
            self.current_condition = current['description'].capitalize()
            self.condition_label.text = self.current_condition
            
            self.current_humidity = f"{current['humidity']}%"
            self.humidity_label.text = self.current_humidity
            
            self.current_wind = f"{current['wind_speed']} m/s"
            self.wind_label.text = self.current_wind
            
            self.current_pressure = f"{current['pressure']} hPa"
            self.pressure_label.text = self.current_pressure
            
            # Update weather icon
            icon_path = self.app.weather_manager.get_weather_icon_path(current['icon'])
            self.weather_image.source = icon_path
            
            # Update forecast
            forecast = weather_data['forecast']
            for i, day_forecast in enumerate(forecast[:5]):
                if i < len(self.forecast_widgets):
                    day_label, day_image, day_temp = self.forecast_widgets[i]
                    
                    # Format date
                    date = datetime.strptime(day_forecast['date'], '%Y-%m-%d')
                    day_name = date.strftime('%a')
                    day_label.text = day_name
                    
                    # Set icon
                    icon_path = self.app.weather_manager.get_weather_icon_path(day_forecast['icon'])
                    day_image.source = icon_path
                    
                    # Set temperature
                    day_temp.text = f"{day_forecast['min_temp']}°C / {day_forecast['max_temp']}°C"
    
    def update_sensor_data(self, sensor_data):
        """Update indoor sensor data display"""
        if sensor_data:
            self.indoor_temp = f"{sensor_data['temperature']}°C"
            self.indoor_temp_label.text = self.indoor_temp
            
            self.indoor_humidity = f"{sensor_data['humidity']}%"
            self.indoor_humidity_label.text = self.indoor_humidity
            
            self.indoor_pressure = f"{sensor_data['pressure']} hPa"
            self.indoor_pressure_label.text = self.indoor_pressure
            
            # Air quality
            air_quality = sensor_data.get('air_quality', 0)
            quality_text = "Unknown"
            
            if air_quality > 80:
                quality_text = "Excellent"
            elif air_quality > 60:
                quality_text = "Good"
            elif air_quality > 40:
                quality_text = "Fair"
            elif air_quality > 20:
                quality_text = "Poor"
            else:
                quality_text = "Bad"
            
            self.indoor_air_quality = quality_text
            self.indoor_air_label.text = self.indoor_air_quality
    
    def show_location_input(self):
        """Show popup for manual location input"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text="Please enter your location:"))
        
        # City input
        city_box = BoxLayout(size_hint=(1, None), height=40)
        city_box.add_widget(Label(text="City:", size_hint=(0.3, 1)))
        city_input = TextInput(multiline=False)
        city_box.add_widget(city_input)
        content.add_widget(city_box)
        
        # Country input
        country_box = BoxLayout(size_hint=(1, None), height=40)
        country_box.add_widget(Label(text="Country:", size_hint=(0.3, 1)))
        country_input = TextInput(multiline=False)
        country_box.add_widget(country_input)
        content.add_widget(country_box)
        
        # Buttons
        buttons = BoxLayout(size_hint=(1, None), height=40)
        cancel_button = Button(text="Cancel")
        submit_button = Button(text="Submit")
        buttons.add_widget(cancel_button)
        buttons.add_widget(submit_button)
        content.add_widget(buttons)
        
        popup = Popup(title="Enter Location", content=content, size_hint=(0.8, 0.4))
        
        # Bind buttons
        cancel_button.bind(on_press=popup.dismiss)
        submit_button.bind(on_press=lambda x: self.submit_location(city_input.text, country_input.text, popup))
        
        popup.open()
    
    def submit_location(self, city, country, popup):
        """Submit manual location"""
        if city and country:
            # Set location
            if self.app.location_manager.set_manual_location(city, country):
                # Update weather
                location = self.app.location_manager.location
                self.app.weather_manager.update_weather(location)
                
                # Update display
                Clock.schedule_once(self.update_weather, 1)
            
            # Close popup
            popup.dismiss()
    
    def open_settings(self, instance):
        """Open settings screen"""
        self.app.sm.current = 'settings'
