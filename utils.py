import json

def get_config():
    # Get Config
    config = None
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    return config