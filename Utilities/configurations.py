import configparser
import os

def getConfig():
    config = configparser.ConfigParser()

    # Get absolute path of config.ini
    config_path = os.path.join(os.path.dirname(__file__), "pytest.ini")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config.read(config_path)

    if "API" not in config:
        raise KeyError("Missing 'API' section in pytest.ini")

    return config
