import os
import json

class ConfigJSONHandler:
    def __init__(self, config_file, config_key):
        self.config_file = config_file
        self.configuration_data = self._load_config(self.config_file, config_key)

    def _load_config(self, config_file, config_key):
        with open(os.path.join(os.path.dirname(__file__),config_file), 'r') as file:
            return json.load(file).get(config_key)
        
    def openJsonFile(self, jsonFile):
        with open(os.path.join(os.path.dirname(__file__),jsonFile), 'r') as file:
            return json.load(file)    

    def get_config(self, key, default=None):
        return self.configuration_data.get(key, default)
    
    def reformat_json(self, data):
        response_data = data.json()
        reformatedData = json.dumps(response_data, indent=2)
        return json.loads(reformatedData)
    
    def get_current_configurations(self):
        output = ''''''
        for entry in self.configuration_data:
            if 'api' in entry.lower() and 'key' in entry.lower():
                output += ('> **'+entry+'**' + ' : ' + '*Hidden*') + '\n'
            else:
                output += ('> **'+entry+'**' + ' : ' + str(self.configuration_data.get(entry))) + '\n'
        return output
    
    def get_response_from_configuration_change(self, config, value, dict):
        configs = self.openJsonFile(self.config_file).get(dict)
        for entry in configs:
            if config.lower() == entry.lower():
                if isinstance(value, int):
                    value = int(value)
                configs[entry] = value
                with open(os.path.join(os.path.dirname(__file__),self.config_file), "w") as file:
                    json.dump({dict : configs}, file, indent=2)
                    return "> Configuration has been updated. Please reload cog."
        return "> The requested configuration has not been found."