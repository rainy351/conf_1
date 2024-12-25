import csv
from datetime import datetime


class Logger:
    def __init__(self, log_path, user):
        self.log_path = log_path
        self.user = user
        self.log_file = open(self.log_path, "a", newline="")
        self.csv_writer = csv.writer(self.log_file)

    def log(self, command, arguments):
        timestamp = datetime.now().isoformat()
        self.csv_writer.writerow([timestamp, self.user, command, " ".join(arguments)])
        self.log_file.flush()

    def __del__(self):
        self.log_file.close()
