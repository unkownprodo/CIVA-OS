from dataclasses import dataclass, field
from typing import Callable, Optional

from core.logger import Logger
from core.persistence import Persistence


# -----------------------------
# DATA STRUCTURES
# -----------------------------

@dataclass
class LogEntry:
    timestamp: str
    command: str
    metadata: Optional[dict] = field(default=None)


@dataclass
class Event:
    kind: str
    payload: dict = field(default_factory=dict)


@dataclass
class CommandEntry:
    description: str
    handler: Callable
    mutates_state: bool = False
    emits_log: bool = True
    modifies_control_flow: bool = False


# -----------------------------
# SHELL CORE
# -----------------------------

class Shell:
    def __init__(self):
        self._log = []
        self._registry = {}
        self._running = True
        self._command_count = 0

        self._readonly_mode = False
        self._protected_mode = False

        self.logger = Logger()
        self.persistence = Persistence()

        # restore previous session if available
        self._restore_session()

    # -------------------------
    # RESTORE SYSTEM
    # -------------------------

    def _restore_session(self):
        data = self.persistence.load()
        if not data:
            return

        state = data.get("state", {})
        log = data.get("log", [])

        self._readonly_mode = state.get("readonly", False)
        self._protected_mode = state.get("protected", False)
        self._command_count = state.get("commands", 0)

        for entry in log:
            self.logger._entries.append(
                type("L", (), entry)()
            )

        print("[SYS] Previous session restored.")

    # -------------------------
    # MAIN LOOP
    # -------------------------

    def run(self):
        print("CIVA-OS Shell starting...")

        while self._running:
            try:
                cmd = input("civa-os> ").strip()
                if not cmd:
                    continue
                self._dispatch(cmd)

            except EOFError:
                self._handle_event("EOF", Event("shutdown", {}))

    # -------------------------
    # DISPATCH
    # -------------------------

    def _dispatch(self, raw: str):
        self._command_count += 1
        self.logger.log(raw)

        parts = raw.split()
        cmd, args = parts[0], parts[1:]

        entry = self._registry.get(cmd)

        if not entry:
            print(f"[SYS] Unknown command: {cmd}")
            return

        try:
            self._check_capabilities(cmd, entry)
            event = entry.handler(args)
            self._handle_event(raw, event)

        except PermissionError:
            return

    # -------------------------
    # CAPABILITY CHECK
    # -------------------------

    def _check_capabilities(self, name, entry: CommandEntry):

        if entry.mutates_state and self._readonly_mode:
            print(f"[SYS] Permission denied: '{name}' mutates state and readonly mode is on.")
            raise PermissionError()

        if entry.modifies_control_flow and self._protected_mode:
            print(f"[SYS] Permission denied: '{name}' modifies control flow and protected mode is on.")
            raise PermissionError()

    # -------------------------
    # EVENT HANDLER
    # -------------------------

    def _handle_event(self, raw: str, event: Event):
        ts = "now"

        if event.kind == "noop":
            return

        if event.kind == "logged":
            self._log.append(LogEntry(ts, raw))

        elif event.kind == "echo":
            self._log.append(LogEntry(ts, event.payload.get("message", "")))

        elif event.kind == "shutdown":
            self._log.append(LogEntry(ts, "shutdown"))

            # persist state before exit
            self.persistence.save(
                self.logger,
                {
                    "readonly": self._readonly_mode,
                    "protected": self._protected_mode,
                    "commands": self._command_count
                }
            )

            self._running = False