from core.shell import Event, CommandEntry


def register_commands(shell):

    def help_cmd(args):
        print("\nAvailable Commands:")
        for name, entry in shell._registry.items():
            print(f"  {name:<10} - {entry.description}")
        return Event("logged", {})

    def status_cmd(args):
        print("\n--- CIVA-OS STATUS ---")
        print(f"Commands: {len(shell._registry)}")
        print(f"Running: {shell._running}")
        print(f"Readonly: {shell._readonly_mode}")
        print(f"Protected: {shell._protected_mode}")
        print("----------------------\n")
        return Event("logged", {})

    def echo_cmd(args):
        message = " ".join(args)
        print(message)
        return Event("echo", {"message": message})

    def exit_cmd(args):
        print("Shutting down...")
        return Event("shutdown", {})

    def syslog_cmd(args):
        print("\n--- SYSLOG ---")
        for entry in shell.logger.get_all():
            print(f"{entry.timestamp:.2f} | {entry.command}")
        print("--------------\n")
        return Event("logged", {})

    shell._registry = {
        "help": CommandEntry("List commands", help_cmd),
        "status": CommandEntry("Show system status", status_cmd),
        "echo": CommandEntry("Print message", echo_cmd),
        "exit": CommandEntry("Shutdown system", exit_cmd),
        "syslog": CommandEntry("Show session history", syslog_cmd),
    }
     