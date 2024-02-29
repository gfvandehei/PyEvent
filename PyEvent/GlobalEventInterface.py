from concurrent.futures import ThreadPoolExecutor
from typing import Dict
import re

class GlobalEventInterface(object):

    def __init__(self):
        self._event_listeners: Dict[str, Any] = {}

    def listen(self, event_regex_exp):
        if event_regex_exp in self._event_listeners:
            self._event_listeners[event_regex_exp].
        pass

    def produce(self, event_path, event_data):
        pass
    