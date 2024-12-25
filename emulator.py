import argparse
import os
from filesystem import VirtualFileSystem
from commands import CommandExecutor
from logger import Logger


def main():
    parser = argparse.ArgumentParser(description="Shell Emulator.")
    parser.add_argument("-u", "--user", default="guest", help="Username")
    parser.add_argument("-o", "--host", default="localhost", help="Hostname")
    parser.add_argument("-f", "--fs", required=True, help="Path to tar archive")
    parser.add_argument("-l", "--log", default="emulator.log", help="Path to log file")
    args = parser.parse_args()

    vfs = VirtualFileSystem(args.fs)
    logger = Logger(args.log, args.user)
    executor = CommandExecutor(vfs, logger)

    while True:
        try:
            prompt = f"{args.user}@{args.host}:{vfs.pwd}> "
            command_line = input(prompt).strip()

            if not command_line:
                continue

            command, *arguments = command_line.split()
            if command == "exit":
                break
            executor.execute(command, arguments)
        except KeyboardInterrupt:  # For Ctrl+C
            print("\nExiting...")
            break
        except EOFError:  # For Ctrl+D
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
