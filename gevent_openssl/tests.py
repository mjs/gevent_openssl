from __future__ import print_function

from gevent import monkey
monkey.patch_all(thread=False)
import gevent
import gevent.socket

import gevent_openssl
gevent_openssl.monkey_patch()

import socket
import time
from OpenSSL import SSL


def lame_connection_test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    sock = socket.create_connection(('www.google.com', 443), timeout=2)
    connection = SSL.Connection(context, sock)
    connection.set_connect_state()
    connection.do_handshake()
    connection.send('GET / HTTP/1.1\r\n\r\n')
    resp = connection.recv(1024)
    if "The document has moved" in resp:
        print("Connection test OK")
    else:
        print("Connection test FAIL. Got: %r" % resp)


def lame_timeout_test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    sock = socket.create_connection(('slashdot.org', 80), timeout=2)
    connection = SSL.Connection(context, sock)
    connection.set_connect_state()
    t0 = time.time()
    try:
        connection.do_handshake()
    except socket.timeout:
        print("timed out in:", time.time() - t0)
    else:
        print("didn't time out!")


def test():
    tests = [
        lame_connection_test,
        lame_timeout_test,
    ]
    gevent.joinall([gevent.spawn(t) for t in tests])

if __name__ == '__main__':
    test()
