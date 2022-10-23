import shlex
import subprocess
import logging

class Execte:
    def __init__(self, command):
        self.command = command
        self.stdout = None
        self.stderr = None
        self.returncode = None

    def do(self):
        args = shlex.split(self.command)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
