

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO as StringIO

import socketserver
import sys
from os import curdir, sep
import os
import subprocess
import cx_Oracle
#os.environ['LD_LIBRARY_PATH'] = "/usr/lib/oracle/12.1/client64/lib"
conn = cx_Oracle.connect('connection string')
document_root = "www"




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
            path = sep+"index.py"

        with open(document_root + path)  as rnf:
            try:
                str = rnf.read()
                old_stdout = sys.stdout
                result = StringIO()
                sys.stdout = result
                exec(str)
                result_string = result.getvalue()
                self.response.write(result_string)
                result.close()
                
            except:
                self.response.write(sys.exc_info()[1])
          
        
class HTTPReponseHandler:
    def __init__(self,request):
        self.request = request
        self.isFile = False
        self.mimetype='text/html'

        if self.request.path.endswith(".html"):
            self.mimetype='text/html'
            self.isFile = True
        if self.request.path.endswith(".jpg"):
            self.mimetype='image/jpg'
            self.isFile = True
        if self.request.path.endswith(".png"):
            self.mimetype='image/png'
            self.isFile = True
        if self.request.path.endswith(".gif"):
            self.mimetype='image/gif'
            self.isFile = True
        if self.request.path.endswith(".js"):
            self.mimetype='application/javascript'
            self.isFile = True
        if self.request.path.endswith(".json"):
            self.mimetype='text/javascript'
            self.isFile = True
        if self.request.path.endswith(".css"):
            self.mimetype='text/css'
            self.isFile = True
        if self.request.path.endswith(".ico"):
            self.mimetype='image/ico'
            self.isFile = True

    def htmlHeader(self):
        self.request.send_response(200)
        self.request.send_header('Content-type',self.mimetype)
        self.request.send_header('Access-Control-Allow-Origin',"*")
        self.request.end_headers()

    def write(self,text):
        self.htmlHeader()
        self.request.wfile.write(bytes(text, "utf8"))

    def writeByte(self,byte):
        self.htmlHeader()
        self.request.wfile.write(byte)

    def runScript(self):
        if self.request.path.endswith(".php"):
            self.runPhp()
        else:    
            script = PythonScriptHandler(self.request,self)
            script.runScript()

    def runPhp(self):
        script = PythonScriptHandler(self.request,self)
        script.runPhp()
        
        #self.write("SHRAVAN")

    def echoFile(self):
        if self.isFile == True:
            
            try:
                f = open(document_root + self.request.path,"rb") 
                self.request.send_response(200)
                self.request.send_header('Content-type',self.mimetype)
                self.request.end_headers()
                #self.request.wfile.write(f.read())
                self.request.wfile.write(f.read())
                f.close()
            except:
                self.request.send_response(404)
                print("File not found")
                #self.request.wfile.write(bytes("File not found", "utf8"))
        return

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        response = HTTPReponseHandler(self)
        if response.isFile == True:
            response.echoFile()
        else:
            response.runScript()

    def do_HEAD(self):
        self._set_headers()
    def do_POST(self):
        response = HTTPReponseHandler(self)
        if response.isFile:
            response.echoFile()
        else:
            response.runScript()
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
    
