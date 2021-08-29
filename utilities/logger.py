import time
import platform
import os

from configparser import Error
from datetime import datetime
from settings.app_config import AppConfig

class Logger():
    _log_to_file = None
    _file_path = None

    def __init__(self):
        self._log_to_file = AppConfig().get_log_to_file()
        file_path = AppConfig().get_log_file_path()

        if self._log_to_file and (".log" not in file_path):
            raise Error("Log file should be of type *.log")
        else:
            self._file_path = file_path

    @staticmethod
    def clear_console():
        system = platform.system()
        if system == 'Windows':
            os.system('cls')
        elif system == 'Linux':
            os.system('clear')
        else:
            raise Exception(f"Unknown operating system detected, can't clear console. [{os}]")

    def console(self, msg=""):
        print(msg)

    def write_to_file(self, level, msg):
        if not self._log_to_file or self._file_path is None:
            pass

        file = open(self._file_path,"a", encoding="utf-8")
        file.write(f"Timestamp [{datetime.utcnow()}] Level [{level}] >> {msg}\n")
        file.close()
    
    def info(self, msg):
        print(f"Timestamp [{datetime.utcnow()}] Level [Info] >> {msg}")
        self.write_to_file("Info", msg)

    def warn(self, msg, delay = 0):
        self.write_to_file("Warning", msg)
        print(f"Timestamp [{datetime.utcnow()}] Level [Warn] >> {msg}")
        if delay > 0:
            time.sleep(delay)
          
    def error(self, msg):
        self.write_to_file("Error", msg)
        print(f"Timestamp [{datetime.utcnow()}] Level [Error] >> {msg}")
        time.sleep(5)
        
