import subprocess
import logging
import os

class Execte:
    def __init__(self, command, isBackground=False):
        self.command = command
        self.isBackground=isBackground
        self.stdout = None
        self.stderr = None
        self.returncode = None

    def do(self):
        if self.isBackground:
            self.returncode=os.system(self.command)
        else:
            popen = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True, close_fds=False)
            popen.wait()
            self.stdout, self.stderr = popen.communicate()
            self.returncode = popen.returncode
        return (self.returncode, self.stdout, self.stderr)
    
    def print(self):
        if self.returncode != 0:
            logging.error(self.stderr)
        else:
            logging.info(self.stdout)

    def isSuccess(self):
        if self.returncode != 0:
            return False
        else:
            return True
