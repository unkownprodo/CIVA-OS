from core.shell import Shell
from core.commands import register_commands


def start_system():
    print("================================")
    print("      CIVA-OS INITIALIZING      ")
    print("================================")

    shell = Shell()

    # register command system BEFORE running
    register_commands(shell)

    shell.run()