import os


class CommandExecutor:
    def __init__(self, vfs, logger):
        self.vfs = vfs
        self.logger = logger

    def execute(self, command, arguments):
        if command == "ls":
            self.ls(arguments)
        elif command == "cd":
            self.cd(arguments)
        elif command == "tail":
            self.tail(arguments)
        elif command == "find":
            self.find(arguments)
        elif command == "help":
            self.help()
        else:
            print(f"Command not found: {command}")
        self.logger.log(command, arguments)

    def ls(self, arguments):
        path = arguments[0] if arguments else self.vfs.pwd
        items = self.vfs.list_directory(path)
        if items:
            print("  ".join(items))
        else:
            print(f"Can not find directory {path}")

    def cd(self, arguments):
        if not arguments:
            return
        path = arguments[0]
        if self.vfs.change_directory(path):
            return
        print(f"Can not change to {path}")

    def tail(self, arguments):
        if not arguments:
            print("Usage: tail <filename>")
            return
        filename = arguments[0]
        content = self.vfs.get_file_content(filename)
        if content is None:
            print(
                f"tail: cannot open '{filename}' for reading: No such file or directory"
            )
            return
        lines = content.splitlines()
        for line in lines[-10:]:
            print(line)

    def find(self, arguments):
        if not arguments:
            print("Usage: find <filename>")
            return
        filename = arguments[0]
        results = self._find_recursive(self.vfs.root, self.vfs.pwd, filename)
        if results:
            for result in results:
                print(result)

    def _find_recursive(self, current_node, current_path, filename):
        results = []
        if isinstance(current_node, dict):
            for key, value in current_node.items():
                new_path = (
                    current_path + "/" + key if current_path != "/fs" else "/" + key
                )
                if isinstance(value, dict):
                    results.extend(self._find_recursive(value, new_path, filename))
                elif key == filename:
                    results.append(new_path)
        return results

    def help(self):
        print("Available commands:")
        print("  ls [path]     - List directory contents (current dir if no path)")
        print("  cd <path>     - Change directory")
        print("  tail <file>   - Display the last 10 lines of a file")
        print("  find <file>   - Search for file and show the path")
        print("  help          - Show this help message")
