# context_manager.py
import json

class ContextManager:
    def __init__(self):
        self.history = []

    def append(self, item):
        self.history.append(item)

    def get_context(self):
        return self.history

    def to_json(self):
        return json.dumps(self.history, indent=2)

