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