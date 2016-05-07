import json

CONFIG_FILE = "/etc/dailyreads/config.json"

Config = {}

try:
    with open(CONFIG_FILE) as json_data_file:
        Config = json.load(json_data_file)
except Exception as e:
    print("Unable to load Configuration file")
    raise e
