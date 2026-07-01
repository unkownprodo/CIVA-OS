from dataclasses import dataclass, field
from typing import List, Optional
from time import time


@dataclass
class LogEntry:
    timestamp: float
    command: str
    metadata: Optional[dict] = field(default=None)


class Logger:
    def __init__(self):
        self._entries: List[LogEntry] = []

    def log(self, command: str, metadata: Optional[dict] = None):
        entry = LogEntry(
            timestamp=time(),
            command=command,
            metadata=metadata
        )
        self._entries.append(entry)

    def get_all(self):
        return self._entries

    def clear(self):
        self._entries.clear()