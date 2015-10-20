from __future__ import print_function

from gevent import monkey
monkey.patch_all(thread=False)
import gevent
import gevent.socket

import gevent_openssl
gevent_openssl.monkey_patch()

import os
import socket
import time
from OpenSSL import SSL


def lame_connection_test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    sock = socket.create_connection(('www.google.com', 443), timeout=2)
    connection = SSL.Connection(context, sock)
    connection.set_connect_state()
    connection.do_handshake() # XXX not needed?
    connection.sendall('GET / HTTP/1.1\r\n\r\n')
    resp = connection.recv(1024)
    if "The document has moved" in resp:
        print("Connection test OK")
    else:
        print("Connection test FAIL. Got: %r" % resp)


def lame_timeout_test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    sock = socket.create_connection(('slashdot.org', 80), timeout=1)
    connection = SSL.Connection(context, sock)
    connection.set_connect_state() # XXX not needed?
    t0 = time.time()
    try:
        connection.do_handshake()
    except socket.timeout:
        print("Timeout test OK (%s)" % (time.time() - t0))
    else:
        print("Timeout test FAIL")

def here(p):
    return os.path.join(os.path.dirname(__file__), p)

def lame_server_test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    context.use_privatekey_file(here('server.key'))
    context.use_certificate_file(here('server.cer'))
    context.load_verify_locations(here('root.cer'))
    server = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server.bind(('localhost', 0))
    port = server.getsockname()[1]

    def run_server():
        server.listen(3)
        conn, _ = server.accept()
        conn.set_accept_state()
        conn.send("foo")
        conn.shutdown()
        conn.close()
        server.close()

    def run_client():
        context = SSL.Context(SSL.TLSv1_METHOD)
        sock = socket.create_connection(('localhost', port), timeout=2)
        conn = SSL.Connection(context, sock)
        conn.set_connect_state()
        resp = conn.recv(32)
        conn.shutdown()
        conn.close()
        print("Server test " + "OK" if resp == "foo" else "FAIL")

    gserver = gevent.spawn(run_server)
    gclient = gevent.spawn(run_client)
    gevent.joinall([gserver, gclient])

def test():
    tests = [
        lame_connection_test,
        lame_timeout_test,
        lame_server_test,
    ]
    gevent.joinall([gevent.spawn(t) for t in tests])

if __name__ == '__main__':
    test()
