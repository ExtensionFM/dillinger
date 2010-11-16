# The Dillinger Tornado

Currently, this is just a proof of concept. But, to try it out first install ZeroMQ, then PyZMQ and then install the ExtensionFM fork of Tornado.

After that's completed, helloworldo.py can be turned on and it can start answering http requests. They will wait for a zmq response until req_handler.py is turned on. Once that's up, the zmq messages go from the tornado instance in helloworld.py to req_handler, back out from req_handler to helloworldo and then back to the browser.

I use the asyncrhonous decorator in Tornado to wait on the zmq sockets and use a map of msg_id's to request handlers to go from the zmq socket back out to clients.

Hopefully this project will improve and become a full framework for using tornado, asynchronous messaging and some sort of document oriented data store.
