from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
class StaticServer(ThreadingHTTPServer):
    request_queue_size=256
class Handler(SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
StaticServer(('127.0.0.1',8422),partial(Handler,directory='docs')).serve_forever()
