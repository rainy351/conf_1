import unittest
import os
import tarfile
from io import BytesIO, StringIO
from unittest.mock import patch
from emulator import main
from filesystem import VirtualFileSystem
from commands import CommandExecutor
from logger import Logger


class TestEmulator(unittest.TestCase):

    def setUp(self):
        # Create a dummy tar archive for testing
        self.test_tar = "unitest_fs.tar"
        with tarfile.open(self.test_tar, "w") as tar:
            # Create in memory files
            file1_content = (
                "This is file1 line1\nThis is file1 line2\nThis is file1 line3"
            )
            file2_content = "This is file2 line1\nThis is file2 line2"
            file3_content = "This is file3 line1"
            # Create in memory tarinfo for the files
            file1_tarinfo = tarfile.TarInfo(name="fs/dir1/file1.txt")
            file1_tarinfo.size = len(file1_content.encode("utf-8"))
            file2_tarinfo = tarfile.TarInfo(name="fs/dir1/file2.txt")
            file2_tarinfo.size = len(file2_content.encode("utf-8"))
            file3_tarinfo = tarfile.TarInfo(name="fs/dir2/file3.txt")
            file3_tarinfo.size = len(file3_content.encode("utf-8"))
            # Add files
            tar.addfile(file1_tarinfo, fileobj=BytesIO(file1_content.encode("utf-8")))
            tar.addfile(file2_tarinfo, fileobj=BytesIO(file2_content.encode("utf-8")))
            tar.addfile(file3_tarinfo, fileobj=BytesIO(file3_content.encode("utf-8")))

            # Create dummy directories
            dir1_tarinfo = tarfile.TarInfo(name="fs/dir1")
            dir1_tarinfo.type = tarfile.DIRTYPE
            tar.addfile(dir1_tarinfo)
            dir2_tarinfo = tarfile.TarInfo(name="fs/dir2")
            dir2_tarinfo.type = tarfile.DIRTYPE
            tar.addfile(dir2_tarinfo)
        self.log_file = "test_emulator.log"
        self.vfs = VirtualFileSystem(self.test_tar)
        self.logger = None

    def tearDown(self):
        if os.path.exists(self.test_tar):
            os.remove(self.test_tar)
        if os.path.exists(self.log_file):
            with open(self.log_file, "w"):  # Clear the file
                pass

    def test_ls_command(self):
        self.logger = Logger(self.log_file, "testuser")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor = CommandExecutor(self.vfs, self.logger)
            self.executor.execute("ls", [])
            self.assertEqual(fake_out.getvalue().strip(), "dir1  dir2")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor = CommandExecutor(self.vfs, self.logger)
            self.executor.execute("ls", ["dir1"])
            self.assertEqual(fake_out.getvalue().strip(), "file1.txt  file2.txt")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor = CommandExecutor(self.vfs, self.logger)
            self.executor.execute("ls", ["non_existent_dir"])
            self.assertEqual(
                fake_out.getvalue().strip(), "Can not find directory non_existent_dir"
            )
        self.logger = None

    def test_cd_command(self):
        self.logger = Logger(self.log_file, "testuser")
        self.executor = CommandExecutor(self.vfs, self.logger)
        self.executor.execute("cd", ["dir1"])
        self.assertEqual(self.vfs.pwd, "/fs/dir1")
        self.executor.execute("cd", [".."])
        self.assertEqual(self.vfs.pwd, "/fs")
        self.executor.execute("cd", ["non_existent_dir"])
        self.assertEqual(self.vfs.pwd, "/fs")
        self.logger = None

    def test_tail_command(self):
        self.logger = Logger(self.log_file, "testuser")
        self.executor = CommandExecutor(self.vfs, self.logger)
        self.executor.execute("cd", ["dir1"])
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor.execute("tail", ["file1.txt"])
            expected_output = (
                "This is file1 line1\nThis is file1 line2\nThis is file1 line3"
            )
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor.execute("tail", ["non_existent_file"])
            expected_output = "tail: cannot open 'non_existent_file' for reading: No such file or directory"
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())
        self.logger = None
        self.executor.execute("cd", [".."])

    def test_find_command(self):
        self.logger = Logger(self.log_file, "testuser")
        self.executor = CommandExecutor(self.vfs, self.logger)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor.execute("find", ["file3.txt"])
            self.assertEqual(fake_out.getvalue().strip(), "/dir2/file3.txt")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor.execute("find", ["non_existent_file.txt"])
            self.assertEqual(fake_out.getvalue().strip(), "")
        self.logger = None

    def test_help_command(self):
        self.logger = Logger(self.log_file, "testuser")
        self.executor = CommandExecutor(self.vfs, self.logger)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor.execute("help", [])
            expected_output = """Available commands:
  ls [path]     - List directory contents (current dir if no path)
  cd <path>     - Change directory
  tail <file>   - Display the last 10 lines of a file
  find <file>   - Search for file and show the path
  help          - Show this help message"""
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())
        self.logger = None

    def test_unknown_command(self):
        self.logger = Logger(self.log_file, "testuser")
        self.executor = CommandExecutor(self.vfs, self.logger)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.executor.execute("unknown_command", [])
            self.assertEqual(
                fake_out.getvalue().strip(), "Command not found: unknown_command"
            )
        self.logger = None

    def test_logger_integration(self):
        with open(self.log_file, "w"):  # Clear the log file
            pass
        self.logger = Logger(self.log_file, "testuser")
        self.executor = CommandExecutor(self.vfs, self.logger)
        self.executor.execute("ls", [])
        self.executor.execute("cd", ["dir1"])
        with open(self.log_file, "r") as log:
            lines = log.readlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("ls", lines[0])
            self.assertIn("cd", lines[1])
            self.assertIn("testuser", lines[0])
            self.assertIn("testuser", lines[1])
        self.logger = None

    @patch("sys.argv", ["emulator.py", "-f", "unitest_fs.tar"])
    def test_emulator_main_integration(self):
        test_input = "ls\nexit\n"
        with patch("sys.stdin", StringIO(test_input)), patch(
            "sys.stdout", new=StringIO()
        ) as fake_out:
            main()
        self.assertIn("dir1  dir2", fake_out.getvalue().strip())
        self.assertTrue(os.path.exists("emulator.log"))


if __name__ == "__main__":
    unittest.main()
