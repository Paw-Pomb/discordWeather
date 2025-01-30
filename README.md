# Weather Bot Cog

This cog utilizes the GeoCoding API, the National Weather Service's API and requires an API key from [geocode.maps.co](https://geocode.maps.co/).

## Setup

1. Create an account at [geocode.maps.co](https://geocode.maps.co/) to obtain an API key.
2. Open the `config.json` file located in the `config_files` folder.
3. Paste your API key into the `geoCodingAPIKey` field.

## Commands

### Weather Command

- **`<command-prefix>weather <zip-code>`**  
  Returns an hourly weather report. The number of items returned is determined by the `hourlyForecastRange` configuration in `config.json`.
  
  **Example:**  
  ```
  !weather 90210
  ```

## Admin-Only Commands

### View Configuration

- **`<command-prefix>weatherAdminConfigs`**  
  Returns the list of configurations from `config.json`.
  
  **Example:**  
  ```
  !weatherAdminConfigs
  ```

### Update Configuration

- **`<command-prefix>setWeatherConfig <configuration> <configuration-value>`**  
  Updates the value of the specified configuration. The configuration must already exist in `config.json`.
  
  **Example:**  
  ```
  !setWeatherConfig hourlyForecastRange 6
  ```

## Notes
- Ensure that your API key is correctly set in `config.json` before running the bot.
- The bot's command prefix should be configured according to your setup.
