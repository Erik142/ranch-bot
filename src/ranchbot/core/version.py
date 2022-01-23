import toml
import os

CONFIG_NAME = "pyproject.toml"

def get_version() -> str:
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, "../", "../", "../", CONFIG_NAME)

    config = toml.load(config_path)

    return config['tool']['poetry']['version']


__version__ = get_version()