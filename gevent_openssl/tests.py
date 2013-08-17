import gevent.monkey
gevent.monkey.patch_all()
import socket
import SSL


def test():
    context = SSL.Context(SSL.TLSv1_METHOD)
    sock = socket.create_connection(('www.google.com', 443), timeout=2)
    connection = SSL.Connection(context, sock)
    connection.set_connect_state()
    connection.do_handshake()
    connection.send('GET / HTTP/1.1\r\n\r\n')
    print(connection.recv(1024))

if __name__ == '__main__':
    test()
