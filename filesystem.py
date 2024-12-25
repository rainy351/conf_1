import tarfile
import os


class VirtualFileSystem:
    def __init__(self, tar_path):
        self.root = {}
        self.pwd = "/fs"
        self._load_tar(tar_path)

    def _load_tar(self, tar_path):
        with tarfile.open(tar_path, "r") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    parts = member.name.split("/")
                    current = self.root
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[parts[-1]] = tar.extractfile(member).read().decode("utf-8")
                elif member.isdir():
                    parts = member.name.split("/")
                    current = self.root
                    for part in parts:
                        if part not in current:
                            current[part] = {}
                        current = current[part]

    def list_directory(self, path=None):
        path = path or self.pwd
        current = self.root
        for part in self._normalize_path(path).split("/")[1:]:
            if part not in current:
                return []
            current = current[part]
        if isinstance(current, dict):
            return list(current.keys())
        else:
            return []

    def change_directory(self, path):
        new_path = self._normalize_path(path)
        current = self.root
        parts = new_path.split("/")[1:]
        if len(parts) == 0:
            self.pwd = new_path
            return True

        current_temp = self.root
        for part in parts[:-1]:
            if part not in current_temp:
                return False
            current_temp = current_temp[part]

        if parts[-1] not in current_temp:
            return False

        if isinstance(current_temp[parts[-1]], dict):
            self.pwd = new_path
            return True
        else:
            return False

    def get_file_content(self, path):
        current = self.root
        for part in self._normalize_path(path).split("/")[1:-1]:
            if part not in current:
                return None
            current = current[part]
        if path.split("/")[-1] not in current:
            return None
        return current[path.split("/")[-1]]

    def _normalize_path(self, path):
        if path.startswith("/"):
            return path
        parts = self.pwd.split("/") + path.split("/")
        parts = [part for part in parts if part and part != "."]

        normalized_parts = []
        for part in parts:
            if part == "..":
                if normalized_parts:
                    normalized_parts.pop()
            else:
                normalized_parts.append(part)

        return "/" + "/".join(normalized_parts)
