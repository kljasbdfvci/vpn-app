import subprocess
import logging
import os

class Execte:
    def __init__(self, command, isBackground=False):
        self.command = command
        self.isBackground = isBackground
        self.stdout = None
        self.stderr = None
        self.returncode = None

    def do(self):
        if self.isBackground:
            self.returncode = os.system(self.command)
        else:
            popen = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True, close_fds=False)
            popen.wait()
            self.stdout, self.stderr = popen.communicate()
            self.returncode = popen.returncode
        return (self.returncode, self.stdout, self.stderr)
    
    def print(self):
        out = "\nexec '{}'.\nexit: {}.".format(self.command, self.returncode)
        s = self.getSTD()
        if s != "":
            out = out + "\n" + s
        if self.returncode != 0:
            logging.error(out)
        else:
            logging.debug(out)

    def getSTD(self):
        s = ""
        if self.stdout != "":
            s = s + self.stdout
        if self.stderr != "":
            if s != "":
                s = s + "\n"
            s = s + self.stderr
        return s

    def isSuccess(self):
        if self.returncode != 0:
            return False
        else:
            return True
