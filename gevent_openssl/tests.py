from gevent import monkey
monkey.patch_all(thread=False)
import gevent

import gevent_openssl
gevent_openssl.monkey_patch()

import socket
from OpenSSL import SSL

def lame_connection_test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    sock = socket.create_connection(('www.google.com', 443), timeout=2)
    connection = SSL.Connection(context, sock)
    connection.set_connect_state()
    connection.do_handshake()
    connection.send('GET / HTTP/1.1\r\n\r\n')
    print(connection.recv(1024))


def test():
    g = gevent.spawn(lame_connection_test)
    g.join()

if __name__ == '__main__':
    test()
