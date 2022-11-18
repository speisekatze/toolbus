# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:19:44 2015

@author: n4p
"""

import http.server
import datetime
import urllib.parse
from importlib import import_module
from src.exceptions import InvalidClusterRole


__version__ = "0.3"

REQOK = 0x0
REQINV = 0x1
SRCINV = 0x2
UNKNOWN = 0x4


def get_help_text():
    """ compile some kind of error page """
    help_html = "<html><head><title>Error</title></head><body>"
    help_html += "<h1>Nope</h1>"
    help_html += "</body>"
    return help_html


class HttpRequest(http.server.BaseHTTPRequestHandler):
    """ simple class to handle our HTTP requests """

    server_version = "httpd/sandbagger " + __version__
    response = []
    logfile = None
    result = []

    def do_GET(self):
        """Serve a GET request."""
        self.send_head()

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.send_head()

    def send_head(self):
        """ currently handles all different requests """
        handler_result = None
        path = urllib.parse.unquote(self.path)
        handler_result = self.process_request(path)
        if handler_result == REQOK:
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=%s" % "UTF-8")
            date = self.date_time_string(
                datetime.datetime.timestamp(datetime.datetime.now())
            )
            self.send_header("Last-Modified", date)

            if len(self.result) > 0:                
                self.send_header("Content-Length", str(len(self.result)))
                self.end_headers()
                self.log_message("served %d bytes" % len(self.result))
                self.wfile.write(self.result.encode("utf8"))
        else:
            if handler_result == REQINV:
                self.send_response(404)
                self.log_message("path not found - path: %s" % path)
            elif handler_result == SRCINV:
                self.send_response(501)
                self.log_message("something went wrong - path: %s" % path)
            else:
                self.send_response(500)
                self.log_message("something went wrong - path: %s" % path)
            help_string = get_help_text()
            self.send_header("Content-type", "text/html; charset=%s" % "UTF-8")
            self.send_header("Content-Length", str(len(help_string)))
            self.end_headers()
            self.wfile.write(help_string.encode("utf8"))

    def process_request(self, path):
        """ Process requests - get blocklist urls from config
            for category name given by request and call aggregator """
        try:
            msg = path.split('?')
            param = ''
            if len(msg) > 1:
                param = msg[1]
            if msg[0] == '/':
                msg[0] = '/init'
            module = 'src.paths' + msg[0].replace('/','.')
            mod = import_module(module)
            self.result = mod.execute(param)
            print(msg)
            return REQOK
        except InvalidClusterRole as error:
            self.log_message(f"Error '{error}' occured.")
            return SRCINV
        else:
            self.log_message("should not get here")
            return UNKNOWN

    def log_message(self, format, *args):
        """ writes message to log """
        address = self.address_string()
        date_time = self.log_date_time_string()
        self.logfile.write("%s - - [%s] %s\n" % (address, date_time, format % args))