#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
import inspect
import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def __str__(self):
        return "'" + str(self.code) + " | " + str(self.body) + "'"

class HTTPClient(object):
    def get_host_port(self,url):
        netloc = urlparse.urlparse(url).netloc
        netloc = netloc.split(':')
        # print('netloc', netloc)
        if (len(netloc) >= 2):
            return netloc[0], int(netloc[1])
        else:
            return netloc[0], 80

    # returns a socket connection
    def connect(self, host, port):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        response = bytearray()
        while True:
            part = sock.recv(1024)
            if (part):
                response.extend(part)
            else:
                break
        print("returning now")
        return str(response)

    def GET(self, url, args=None):
        print("GET | url:" + url)
        host, port = self.get_host_port(url)
        clientSocket = self.connect(host, port)
        request = "GET / HTTP/1.0\r\n\r\n"
        clientSocket.sendall(request)
        data = self.recvall(clientSocket)
        print(data)
        # code = self.get_code(data)
        # headers = self.get_headers(data)   # can we just drop the headers then?
        # body = self.get_body(data)
        code = 500  # replace this with the code above
        body = ""  # replace this with the code above
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
