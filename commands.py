from redbot.core import commands # type: ignore
from discordWeather.config_json_handler import ConfigJSONHandler
from discordWeather.weather_api_handler import WeatherApiHandler
from discordWeather.weather_report_handler import WeatherReportHandler
from discordWeather.logger import Logger
    
class WeatherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_handler = ConfigJSONHandler("config_files/config.json", "base_configs")
        self.weather_report_handler = WeatherReportHandler()
        self.geo_api_key = self.config_handler.get_config("geoCodingAPIKey")
        self.weather_api_handler = WeatherApiHandler(self.geo_api_key)
        self.weather_logger = Logger.setLogger(__name__)
        
    @commands.command()
    async def weather(self, ctx, q: str):
        "Enter a Zip Code to get an Hourly Report."
        hourly_weather_report = self.weather_report_handler.get_hourly_report(q, self.config_handler, self.weather_api_handler, self.weather_logger)
        await ctx.send(hourly_weather_report)