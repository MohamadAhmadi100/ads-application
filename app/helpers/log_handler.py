import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class LogHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        LogHandler.log_folder_create()
        super().__init__(*args, **kwargs)

    def doRollover(self):
        dates = []
        if os.path.isfile("app.log.3"):
            dates.extend(os.path.getmtime(f"app.log.{i}") for i in range(1, 8))
            should_remove = sorted(dates, reverse=True).pop(-1)
            os.remove(f"app.log.{should_remove}")
        super().doRollover()

    @staticmethod
    def log_folder_create():
        if not os.path.exists("logs"):
            os.mkdir("logs")

    def emit(self, record):
        if record.levelname == "ERROR":
            stream = self.stream
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            message = [record.msg]
            msg = str(f"{date} [{record.levelname}] {message[0]}").replace("\n", "")
            stream.write(msg)
            stream.write("\n")
            self.flush()
        super().emit(record)
