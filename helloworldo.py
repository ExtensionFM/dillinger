#!/usr/bin/env python


import uuid
import json
import tornado.httpserver
from tornado import ioloop
import tornado.web
import zmq
#from zmq.eventloop import zmqstream
import zmqstream


class ZMQMixin():
    def zmq_send_msg(self, msg, callback):
        msg_id = self.application.zmq_send_msg(msg, callback)
        
        

class MainHandler(ZMQMixin, tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        msg = 'yt?'
        print 'Sending to request handler: "%s"' % (msg)
        self.zmq_send_msg(msg, self.callback)

    def callback(self, response):
        print 'Received from request handler: %s' % ''.join(response)
        html = "<html>\n<body>\n<h1>%s</h1>\n</body>\n</html>"
        html_page = html % (response)
        self.write(html_page)
        self.finish()
    

        
class ZMQApplication(tornado.web.Application):
    def __init__(self, zmq_stream, handlers, *args, **kwargs):
        super(ZMQApplication, self).__init__(handlers, *args, **kwargs)
        self._zmq_msg_id_map = dict()
        self._zmq_stream = zmq_stream
        self._zmq_stream.on_recv(self._handle_zmq_msg)
        
    def zmq_send_msg(self, msg, callback):
        msg_id = uuid.uuid4().get_hex()
        zmq_msg_data = {
            'msg_id': msg_id,
            'data': msg,
        }
        zmq_msg_json = json.dumps(zmq_msg_data)
        self._zmq_stream.send_multipart(zmq_msg_json)
        self._zmq_msg_id_map[msg_id] = callback

    def _handle_zmq_msg(self, msg):
        zmq_msg_json = ''.join(msg)
        zmq_msg_data = json.loads(zmq_msg_json)
        msg_id = zmq_msg_data['msg_id']
        self._zmq_msg_id_map[msg_id](zmq_msg_data['data'])
        

if __name__ == "__main__":
    print 'Starting'

    loop = ioloop.IOLoop.instance()

    ctx = zmq.Context()
    s = ctx.socket(zmq.REQ)
    s.connect("ipc://127.0.0.1:5678")
    stream = zmqstream.ZMQStream(s, loop)
    
    handlers = [(r"/", MainHandler),]
    application = ZMQApplication(stream, handlers)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    loop.start()


