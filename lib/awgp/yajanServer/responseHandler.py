
import os
from lib.awgp.yajanServer.scriptHandler import PythonScriptHandler
from config import parm

document_root = parm["webroot"]

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
            if os.path.isfile(document_root + self.request.path) :    
                try:
                    f = open(document_root + self.request.path,"rb") 
                    self.request.send_response(200)
                    self.request.send_header('Content-type',self.mimetype)
                    self.request.end_headers()
                    self.request.wfile.write(f.read())
                    f.close()
                except:
                    self.request.send_response(404)
                    
                #self.request.wfile.write(bytes("File not found", "utf8"))
        return
