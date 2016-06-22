#!/usr/bin/env python

import os
import sys
import time
import json
import thread

import rex

from nxtools import *

from hlsm import config
from hlsm import HLSMonitor

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


if __name__ == "__main__":
    server = HTTPServer(
            (config.get("listen_address", ""), config.get("listen_port", 12001)),
            MonitorHandler
            )
    server.monitor = HLSMonitor()
    thread.start_new_thread(server.serve_forever, ())

    while True:
        now = time.time()
        server.monitor.work()
        time.sleep(config.get("loop_delay", 30))

