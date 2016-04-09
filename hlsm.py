#!/usr/bin/env python

import os
import sys
import time
import json
import thread

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
# Vendor imports
#

vendor_dir = os.path.join(app_root, "vendor")
if os.path.exists(vendor_dir):
    for pname in os.listdir(vendor_dir):
        pname = os.path.join(vendor_dir, pname)
        pname = os.path.abspath(pname)
        if not pname in sys.path:
            sys.path.insert(0, pname)

from nxtools import *

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
# API Handler
#

class MonitorHandler(BaseHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        pass

    def do_headers(self, response=200, mime="application/json", headers=[]):
        self.send_response(response)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header('Content-type', mime)
        for key, value in headers:
            handler.send_header(key, value)
        self.end_headers()

    def echo(self, string):
        self.wfile.write(string)

    def result(self, response, data, mime="application/json"):
        self.do_headers(response=response, mime=mime)
        self.echo(data)

    def do_GET(self):
        """
        API Reference
        -------------

        /stream                  List of available streams
        /stream/{stream_name}    Stream metadata
        /result/{stream_name}    Stream probe result

        """

        start_time =  time.time()
        self.path

        result = {}
        self.result(200, json.dumps(result))

#
# Main loop
#

if __name__ == "__main__":
    server = HTTPServer(
            (config.get("listen_address", ""), config.get("listen_port", 12001)),
            MonitorHandler
            )
    server.monitor = HLSMonitor()
    thread.start_new_thread(server.serve_forever, ())

    while True:
        now = time.time()
        if now - config_last_updated > config.get("config_update_time", 60):
            update_config()
            config_last_updated = now
            server.monitor.set_streams(config["streams"])
        server.monitor.work()
        time.sleep(config.get("loop_delay", 30))

