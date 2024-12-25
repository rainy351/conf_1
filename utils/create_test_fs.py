import tarfile
import os


def create_test_tar(tar_path):
    with tarfile.open(tar_path, "w") as tar:
        # Create a test directory
        os.makedirs("test_fs/dir1", exist_ok=True)
        os.makedirs("test_fs/dir1/subdir", exist_ok=True)
        os.makedirs("test_fs/sys", exist_ok=True)
        os.makedirs("test_fs/dir2/subdir/subdir", exist_ok=True)

        # Create test files with content
        with open("test_fs/dir1/file1.txt", "w") as f1:
            f1.write("content of file 1")

        with open("test_fs/dir1/subdir/file2.txt", "w") as f2:
            f2.write("content of file 2")

        with open("test_fs/dir2/subdir/subdir/file3.txt", "w") as f2:
            f2.write("content of file 3")

        with open("test_fs/sys/help.txt", "w") as f2:
            f2.write("COMMANDS:\nls, cd, exit\nfind, tail")

        tar.add("test_fs/dir1", arcname="fs/dir1")
        tar.add("test_fs/dir2", arcname="fs/dir2")
        tar.add("test_fs/sys", arcname="fs/sys")

    import shutil

    shutil.rmtree("test_fs")


create_test_tar("test_fs.tar")
