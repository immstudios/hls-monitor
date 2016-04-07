import time
import requests

from nxtools import *

class Stream():
    def __init__(self):
        self.url = None
        self.title = None

    @property
    def default_title(self):
        self.url.split("/")[-1].split("?")[0]

    def __repr__(self):
        return self.title or self.default_title


class Result():
    def __init__(self):
        self.started = time.time()
        self.current_problems = set()
        self.past_problems = set()

    def reset_problems(self):
        self.problems = {}

    def set_problem(self, key):
        self.current_problems.add(key)

    @property
    def result(self):
        pass




class HLSMonitor():
    def __init__(self):
        self.streams = []
        self.result = {}

    def set_streams(self, data):
        self.streams = []
        for stream_data in data:
            stream = Stream()
            stream.url = stream_data["url"]
            stream.title = stream_data.get("title", None)
            self.streams.append(stream)

    def work(self):
        for stream in self.streams:
            logging.info("Checking stream {}".format(stream))

            manifest_request = requests.get(stream.url)
            print dir(manifest_request)
            if manifest_request.status_code >= 400:
                ]


