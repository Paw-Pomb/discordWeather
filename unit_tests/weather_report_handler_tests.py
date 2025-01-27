import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from weather_report_handler import WeatherReportHandler
from config_json_handler import ConfigJSONHandler
from logger import Logger

class WeatherReportHandlerTest(unittest.TestCase):
    
    config_handler = ConfigJSONHandler("config_files/config.json", "base_configs")
    weather_handler = WeatherReportHandler()
    weather_logger = Logger.setLogger(__name__)
    
    def test_determine_if_state_is_present(self):
        display_name = "Los Angeles, California, United States"
        state = self.weather_handler.determineState(display_name, self.config_handler)
        self.assertEqual(state, ['CA', 'California'])
        
    def test_determine_if_state_is_not_present(self):
        display_name = "Toronto, Canada"
        state = self.weather_handler.determineState(display_name, self.config_handler)
        self.assertIsNone(state)
        
    def test_if_city_can_be_found_with_three_data_variables(self):
        display_name = "Los Angeles, California, United States"
        state = ['CA', 'California']
        county = None
        country = "United States"
        city = self.weather_handler.isolate_city_from_display_name(state, county, display_name, country, self.weather_logger)
        self.assertEqual(city, "Los Angeles")
        
    def test_if_township_can_be_found_with_missing_city(self):
        display_name = "Worth Township, Cook County, Illinois, 60805, United States"
        state = ['IL', 'Illinois']
        county = "Cook County"
        country = "United States"
        city = self.weather_handler.isolate_city_from_display_name(state, county, display_name, country, self.weather_logger)
        self.assertEqual(city, "Worth Township")
        
if __name__ == "__main__":
    unittest.main()