
import sys
import os
import subprocess
from io import StringIO as StringIO
from os import curdir, sep


from config import parm

document_root = parm["webroot"]


class PythonScriptHandler:
    def __init__(self,request,response):
        self.request = request
        self.response = response
        
    def runPhp(self):
        cmd = "php \"www"+self.request.path+"\""
        with subprocess.Popen(["php","www"+self.request.path], stdout=subprocess.PIPE) as proc:
            output = proc.stdout.read() 
            self.response.writeByte(output)

    def runScript(self):
        if self.request.path.endswith(".py"):
            path = self.request.path
        else:
            path = "/index.py"

        
        with open(document_root + path)  as rnf:

            try:
                old_stdout = sys.stdout
                result = StringIO()
                sys.stdout = result
                str = rnf.read()
                exec(str)
                result_string = result.getvalue()
                self.response.write(result_string)
                result.close()
                
            except SyntaxError:
                import traceback
                exc = traceback.format_exc()
                print("Error in "+document_root + path)
                print(exc)
                result_string = result.getvalue()
                self.response.write(result_string)          
        
