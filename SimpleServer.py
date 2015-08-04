#!/usr/bin/python
import os
import sys
import SimpleHTTPServer
import SocketServer
import logging
import cgi
import json
from subprocess import Popen, PIPE, STDOUT

if 'PORT' in os.environ:
    PORT = int(os.environ['PORT'])
    print 'Got port ', PORT
else:
    PORT = 8000


import openPitMining

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/openPitMining.py':
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                for val in data:
                    jsdict = json.loads(val)
                    jsdict = openPitMining.handleoptimize(jsdict)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(jsdict))
                    return
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Starting simple server"
print "serving at port", PORT
httpd.serve_forever()
