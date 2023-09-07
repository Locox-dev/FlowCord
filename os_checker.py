import json
import platform

config_data = []

with open('JSON/config.json', 'r') as json_file:
    config_data = json.load(json_file)


config_data["OS_NAME"] = platform.system()
config_data["OS_VERSION"] = platform.release()
    
with open('JSON/config.json', 'w') as json_file:
    json.dump(config_data, json_file, indent=4)