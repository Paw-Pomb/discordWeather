from datetime import datetime
import requests
import re

class WeatherReportHandler:
    def get_hourly_report(self, query, config_handler, weather_api_handler, weather_logger):
        try:
            output = ''''''
            geolocation_data = weather_api_handler.get_geolocation(query, config_handler)
            if not geolocation_data:
                raise ValueError("No geolocation data found for the query.")
            display_name = geolocation_data.get('display_name')
            
            lat = geolocation_data.get('lat')
            lon = geolocation_data.get('lon')
            
            if not display_name or not lat or not lon:
                raise ValueError("Incomplete geolocation data.")
            display_name_list = display_name.split(',')
            country = display_name_list[len(display_name_list) - 1]
            state = self.determineState(display_name, config_handler)
            county = self.isolate_county_from_display_name(display_name)
            city = self.isolate_city_from_display_name(state, county, display_name, country, weather_logger)
            
            weather_alert_data = weather_api_handler.get_weather_alert_data(state)
            weather_data = weather_api_handler.get_weather_data(lat, lon)
            hourly_weather_response_data = self.get_hourly_forecast_data(weather_data, config_handler)
            weather_alert_output = self.get_weather_alert_output(state, county, city, weather_alert_data, config_handler, weather_logger)
            
            if weather_alert_output != None and len(weather_alert_output) > 0:
                output += "**Weather Alert(s):** \n"
                for alert in weather_alert_output:
                    output += f"{alert}\n"
                output += "\n"
            output += self.format_weather_report(hourly_weather_response_data, city, config_handler, weather_logger)
            return output
        except Exception as e:
            weather_logger.error(f"An error occurred while generating the report: {e}", exc_info=True)
    
    def determineState(self, display_name, config_handler):
        countries_and_states_data = config_handler.openJsonFile('config_files/countries_and_states.json')
        us_states = countries_and_states_data.get('us_states_and_territories')
        determinedState = None
        for entry in us_states:
            if us_states.get(entry) in display_name:
                determinedState = [entry, us_states.get(entry)]
        return determinedState
    
    def get_hourly_forecast_data(self, weather_data, config_handler):         
        hourly_forecast_url = weather_data.get('properties', {}).get("forecastHourly")
        hourly_forecast_data = config_handler.reformat_json(requests.get(hourly_forecast_url))
        periods = hourly_forecast_data.get('properties', {}).get('periods', [])
        forecast_range = config_handler.get_config('hourlyForecastRange')
        return [{"sub_periods": periods[:forecast_range]}]
    
    def get_weather_alert_output(self, state, county, city, weather_alert_data, config_handler, weather_logger):
            headlines = []
            features_data_subset = weather_alert_data.get("features", [])
            county = (
                self.determine_county_from_special_case(city, state, config_handler)
                if not county
                else county
            )

            if county:
                for feature in features_data_subset:
                    properties = feature.get("properties", {})
                    area_desc = properties.get("areaDesc", "")
                    if county in area_desc:
                        headlines.append(properties.get("headline", ""))
                headlines = self.removeAlertHeadlineDuplicates(headlines)
            else:
                weather_logger.info("County not found for " + city)
            return headlines
    
    def isolate_county_from_display_name(self, display_name):
        display_name_list = display_name.split(',')
        for item in display_name_list:
            if "County" in item:
                return item
        return None
        
    def isolate_city_from_display_name(self, state, county, display_name, country, weather_logger):
        display_name_list = display_name.split(',')
        full_state = state[1]
        township = None
        zip_code_regex = r"^\d{5}(?:-\d{4})?$"
        for item in display_name_list[:]:
            if country and (item.lower().strip() == country.lower().strip()):
                display_name_list.remove(item)
            if full_state and (item.lower().strip() == full_state.lower().strip()):
                display_name_list.remove(item)
            if county and (county.lower().strip() == item.lower().strip()):
                display_name_list.remove(item)
            if re.search(zip_code_regex, item.strip()):
                display_name_list.remove(item)
            if "township" in item.lower():
                township = item
                display_name_list.remove(item)
        if len(display_name_list) > 1:
            weather_logger.info(f"Extra item found in data: " + display_name_list[1])
            return display_name_list[0]
        elif len(display_name_list) <= 0 and township != None:
            return township
        else:
            return display_name_list[0]
        
    def determine_county_from_special_case(self, city, state, config_handler):
        full_state = state[1]
        special_case_counties_file = config_handler.openJsonFile("config_files/special_case_counties.json")
        special_case_state_data = special_case_counties_file.get(full_state)
        for key, cities in special_case_state_data.items():
            if city.strip().lower() in map(str.lower, map(str.strip, cities)):
                return key
        return None
    
    def removeAlertHeadlineDuplicates(self, headlines):
        if len(headlines) <= 1:
            return headlines
        advisory_regex = re.compile(r"issued.*")
        time_regex = re.compile(r"\w+ \d{1,2} at \d{1,2}:\d{2}(AM|PM)")
        headlines_dict = {}
        for headline in headlines:
            advisory_match = advisory_regex.search(headline)
            if advisory_match:
                issued = advisory_match.group().strip()
                advisory = headline.replace(issued, "").strip()
                if advisory in headlines_dict:
                    current_time = time_regex.search(issued).group(0)
                    existing_time = time_regex.search(headlines_dict[advisory]).group(0)
                    if self.compare_date_and_time(current_time, existing_time, "prime"):
                        headlines_dict[advisory] = issued
                else:
                    headlines_dict[advisory] = issued
        return [f"{adv} {issued}" for adv, issued in headlines_dict.items()]

    def _convert_time_to_hour(self, start_time):
        dt = datetime.fromisoformat(start_time)
        return dt.strftime("%I:%M %p")

    def compare_date_and_time(self, date1, date2, format):
        if format == "prime":
            date1, date2 = date1.replace("at", ""), date2.replace("at", "")
            dt1 = datetime.strptime(date1, "%B %d %I:%M%p")
            dt2 = datetime.strptime(date2, "%B %d %I:%M%p")
            if dt1 > dt2:
                return True
        return False
    
    def format_weather_report(self, data, city, handler, weather_logger):
        output = ''''''
        output += f"**Hourly Forecast for {city}:** \n"
        sub_periods = data[0]
        emoji_file = handler.openJsonFile("config_files/weatherEmojis.json")
        for entry in sub_periods.get("sub_periods"):
            hour = self._convert_time_to_hour(entry.get('startTime'))
            short_forecast = entry.get("shortForecast")
            emoji = self._determine_emoji(entry.get("isDaytime"), short_forecast, emoji_file, weather_logger)
            temp = f"{entry.get('temperature')}{entry.get('temperatureUnit')}"
            precip = f"{entry.get('probabilityOfPrecipitation').get('value')}%"
            output += f"**{hour}:** {emoji} {short_forecast}, Temp: {temp}, Precip: {precip}\n"
        return output

    def _determine_emoji(self, is_daytime, short_forecast, emoji_file, weather_logger):
        emojiFileDataKey = 'isDaytime' if is_daytime else 'isNotDayTime'
        emojiFileData = emoji_file.get(emojiFileDataKey, {})
        unknownEmoji = emoji_file.get('unknownValue', 'Unknown Emoji')
        emoji = None
        if emojiFileDataKey == 'isDaytime':
            emojiSubData = self.iteratre_through_emoji_data(emojiFileData, short_forecast)
            if emojiSubData == None:
                emojiSubData = emojiFileData.get('standard')
            emoji = self.iteratre_through_emoji_data(emojiSubData, short_forecast)
        else:
            emoji = self.iteratre_through_emoji_data(emojiFileData, short_forecast)
        if emoji is not None:
            return emoji
        else: 
            weather_logger.info("No emoji available for forecast: " + short_forecast)
            return unknownEmoji
    
    def iteratre_through_emoji_data(self, data, forecast):
        for entry in data:
            if entry in forecast.lower():
                return data.get(entry)