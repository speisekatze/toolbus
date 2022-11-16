import time
import src.config as toolbus
from src.handler import HttpRequest
from src.server import HttpServer

print(toolbus.server)

httpd = HttpServer(HttpRequest, int(toolbus.server['port']), toolbus.server['proto'])
httpd.set_cert(toolbus.server['cert'], toolbus.server['key'])
httpd.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server shutting down")
httpd.stop()