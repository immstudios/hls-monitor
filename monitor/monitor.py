import time
import requests

from nxtools import *
from hls import HLSManifest


class Stream():
    def __init__(self):
        self.url = False
        self.name = False

    @property
    def default_name(self):
        return self.url.split("/")[-1].split("?")[0].replace(".m3u8","")

    def __repr__(self):
        return self.name or self.default_name

    def __str__(self):
        return self.__repr__()


class Problem():
    def __init__(self, key, description=None):
        self.time_introduced = time.time()
        self.key = key
        self.description = description

    @property
    def age(self):
        return time.time() - self.time_introduced


class Result():
    def __init__(self):
        self.current_problems = set()
        self.past_problems = set()

    def finish(self):
        self.problems = {}

    def set_problem(self, key):
        self.current_problems.add(key)

    @property
    def result(self):
        pass




class HLSMonitor():
    def __init__(self):
        self.streams = []
        self.results = {}

    def set_streams(self, data):
        self.streams = []
        for stream_data in data:
            stream = Stream()
            stream.url = stream_data["url"]
            stream.name = stream_data.get("name", None)
            self.streams.append(stream)

    def set_problem(self, stream, key, description=None):
        pass


    def work(self):
        for stream in self.streams:
            logging.info("Checking stream {}".format(stream))
            if not stream.name in self.results:
                self.results[stream.name] = Result()

            manifest_request = requests.get(stream.url)
            if manifest_request.status_code >= 400:
                self.set_problem(stream.name, "manifest_unavailable", "Error {}".format(manifest_request.status_code))
                continue

            manifest = HLSManifest(parse=manifest_request.content)

            print manifest.segments

            break

        for stream in self.streams:
            self.results[stream.name].finish()
