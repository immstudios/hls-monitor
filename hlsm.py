#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import time
import json

from nxtools import *
from monitor import HLSMonitor

#
# Env setup
#

if sys.version_info[:2] < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

app_root = os.path.abspath(os.getcwd())
if not app_root in sys.path:
    sys.path.append(app_root)

#
# Configuration
#

config = {}
config_last_updated = 0

def update_config():
    settings_file = os.path.join(app_root, "local_settings.json")
    if os.path.exists(settings_file):
        try:
            config.update(json.load(open(settings_file)))
        except:
            log_traceback()
            critical_error("Unable to parse settings file")

#
# Main loop
#

if __name__ == "__main__":
    monitor = HLSMonitor()

    while True:
        now = time.time()
        if now - config_last_updated > config.get("config_update_time", 60):
            update_config()
            config_last_updated = now
            monitor.set_streams(config["streams"])
        logging.debug("Starting work")
        monitor.work()
        break
        time.sleep(config.get("loop_delay", 30))
