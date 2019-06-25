"""Config values for ilswbot."""
import os
import sys
import toml

default_config = {
    'telegram': {
        "api_key": "your_telegram_api_key",
    },
    'database': {
        "sql_uri": 'sqlite:///ilswbot.db',
    },
    'settings': {
        'api_url': 'http://ilswlol.customalized.org/?raw=on',
        'one_time_subs': True,
        'permanent_subs': False,
    },
    'webhook': {
        "enabled": False,
        "domain": "https://localhost",
        "token": "stickerfinder",
        "cert_path": '/path/to/cert.pem',
        "port": 7000,
    },
}

config_path = os.path.expanduser('~/.config/ilswbot.toml')

if not os.path.exists(config_path):
    with open(config_path, "w") as file_descriptor:
        toml.dump(default_config, file_descriptor)
    print("Please adjust the configuration file at '~/.config/ilswbot.toml'")
    sys.exit(1)
else:
    config = toml.load(config_path)
