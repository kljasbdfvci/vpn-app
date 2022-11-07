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
        out = "\nexec: '{}'.\nexit: '{}'.".format(self.command, self.returncode)
        s = self.getSTD(5)
        if s != "":
            out = out + "\n" + s
        if self.returncode != 0:
            logging.error(out)
        else:
            logging.debug(out)

    def getSTD(self, max_line = None):
        out = ""
        if self.stdout != "":
            if max_line != None and len(self.stdout.splitlines()) > max_line:
                out = out + "stdout: '{}'.".format('\n'.join(self.stdout.splitlines()[-max_line:]))
            else:
                out = out + "stdout: '{}'.".format(self.stdout)
        if self.stderr != "":
            if out != "":
                out = out + "\n"
            if max_line != None and len(self.stderr.splitlines()) > max_line:
                out = out + "stderr: '{}'.".format('\n'.join(self.stderr.splitlines()[-max_line:]))
            else:
                out = out + "stderr: '{}'.".format(self.stderr)
        return out

    def isSuccess(self):
        if self.returncode != 0:
            return False
        else:
            return True
