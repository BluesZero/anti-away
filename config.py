import json

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        if "inactivity_trigger" not in config:
            config["inactivity_trigger"] = 4
        if "enable_auto_trigger" not in config:
            config["enable_auto_trigger"] = True
        return config
    except FileNotFoundError:
        return {
            "interval": 300,
            "auto_start": False,
            "inactivity_trigger": 4,
            "enable_auto_trigger": True
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)