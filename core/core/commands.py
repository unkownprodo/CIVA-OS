from core.shell import Event, CommandEntry


def register_commands(shell):

    def help_cmd(args):
        return Event("logged", {})

    def status_cmd(args):
        print("System running...")
        return Event("logged", {})

    def echo_cmd(args):
        message = " ".join(args)
        print(message)
        return Event("echo", {"message": message})

    def exit_cmd(args):
        print("Shutting down...")
        return Event("shutdown", {})

    shell._registry = {
        "help": CommandEntry("List commands", help_cmd),
        "status": CommandEntry("Show system status", status_cmd),
        "echo": CommandEntry("Print message", echo_cmd),
        "exit": CommandEntry("Shutdown system", exit_cmd),
    }