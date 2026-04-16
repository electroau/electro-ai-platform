import json
import os


class KnowledgeBase:

    def __init__(self):
        base_path = os.path.dirname(__file__)
        knowledge_path = os.path.join(base_path, "../knowledge")

        with open(os.path.join(knowledge_path, "valves.json")) as f:
            self.valves = json.load(f)

    def find_valve(self, text: str):
        text = text.upper()

        for valve in self.valves:
            if valve in text:
                return valve, self.valves[valve]

        return None, None
