import json
from datetime import datetime


class Persistence:
    def __init__(self, path="civa_session.json"):
        self.path = path

    def save(self, logger, shell_state: dict):
        data = {
            "timestamp": datetime.now().isoformat(),
            "state": shell_state,
            "log": [
                {
                    "timestamp": entry.timestamp,
                    "command": entry.command,
                    "metadata": entry.metadata
                }
                for entry in logger.get_all()
            ]
        }

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None