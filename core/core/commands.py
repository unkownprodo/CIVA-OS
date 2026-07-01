from core.shell import Event, CommandEntry


def register_commands(shell):

    def help_cmd(args):
        print("\nAvailable Commands:")
        for name, entry in shell._registry.items():
            print(f"  {name:<12} - {entry.description}")
        return Event("logged", {})

    def status_cmd(args):
        print("\n--- CIVA-OS STATUS ---")
        print(f"Commands loaded: {len(shell._registry)}")
        print(f"Running: {shell._running}")
        print(f"Readonly mode: {shell._readonly_mode}")
        print(f"Protected mode: {shell._protected_mode}")
        print("----------------------\n")
        return Event("logged", {})

    def echo_cmd(args):
        message = " ".join(args)
        print(message)
        return Event("echo", {"message": message})

    def exit_cmd(args):
        print("Shutting down CIVA-OS...")
        return Event("shutdown", {})

    def syslog_cmd(args):
        print("\n--- SYSLOG ---")
        for line in shell.logger.format_entries():
            print(line)
        print("--------------\n")
        return Event("logged", {})

    shell._registry = {
        "help": CommandEntry("List all available commands", help_cmd),
        "status": CommandEntry("Show system status", status_cmd),
        "echo": CommandEntry("Print a message", echo_cmd),
        "exit": CommandEntry("Shutdown system", exit_cmd),
        "syslog": CommandEntry("Show session history", syslog_cmd),
    }