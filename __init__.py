from .commands import WeatherCommands

async def setup(bot):
    await bot.add_cog(WeatherCommands(bot))