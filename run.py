

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import sys
import os
import subprocess
#import cx_Oracle
import socketserver

from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO as StringIO
from os import curdir, sep


from lib.awgp.yajanServer.responseHandler import HTTPReponseHandler
from lib.awgp.yajanServer.scriptHandler import PythonScriptHandler

from config import parm


#os.environ['LD_LIBRARY_PATH'] = "/usr/lib/oracle/12.1/client64/lib"

document_root = parm["webroot"]
db=[]



try:
    os.mkdir(document_root)
except FileExistsError:
    False


if os.path.isfile(document_root+"/index.py")== False:
    pystr = "print(\"It's working\")"
    file = open(document_root+"/index.py","w")
    file.write(pystr)

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
    print ('Starting AWGP Python server on port '+str(port)+'... ')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
    
