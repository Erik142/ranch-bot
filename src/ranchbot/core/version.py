import toml
import os

CONFIG_NAME = "pyproject.toml"

def get_version() -> str:
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, "../", "../", "../", CONFIG_NAME)

    print(config_path)

    config = toml.load(config_path)
    print(config)

    return config['tool']['poetry']['version']


__version__ = get_version()