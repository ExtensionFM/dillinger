#!/usr/bin/env python

import zmq
import json
#from zmq.eventloop import zmqstream
import zmqstream
from tornado import ioloop
loop = ioloop.IOLoop.instance()

ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind('ipc://127.0.0.1:5678')
stream = zmqstream.ZMQStream(s, loop)

def echo(msg):
    msg_json = ''.join(msg)
    print 'Received from Tornado: %s' % msg_json
    msg_data = json.loads(msg_json)
    msg_id = msg_data['msg_id']
    response = {
        'status_code': 200,
        'status_text': 'OK',
        'data': 'what up?',
        'msg_id': msg_id,
    }
    response_json = json.dumps(response)
    print 'Sending back to Tornado: %s' % (response_json)
    stream.send_multipart(response_json)

stream.on_recv(echo)

loop.start()
