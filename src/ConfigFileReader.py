#CLASS TO LOAD INITIAL CONFIGURATION
import yaml

class ConfigFileReader:
    def __init__(self, config_file):
        with open(config_file, 'r') as stream:
            self.config = yaml.safe_load(stream)

    def get_configuration_params(self):
        return self.config