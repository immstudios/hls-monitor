import os
import json

from nxtools.logging import *

__all__ = ["config"]

base_dir = os.path.abspath(os.getcwd())
config_path = os.path.join(base_dir, "local_settings.json")

config = {
        "host" : "",
        "port" : 12001
    }

if os.path.exists(config_path):
    try:
        config.update(json.load(open(config_path)))
    except:
        log_traceback()
        logging.warning("Unable to open configuration file")
