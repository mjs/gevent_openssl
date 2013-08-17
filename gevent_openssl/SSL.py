"""gevent_openssl.SSL - gevent compatibility with OpenSSL.SSL.
"""

import sys
from OpenSSL.SSL import *
from OpenSSL.SSL import WantReadError
from OpenSSL.SSL import WantWriteError
from OpenSSL.SSL import WantX509LookupError
from OpenSSL.SSL import ZeroReturnError
from OpenSSL.SSL import SysCallError
from OpenSSL.SSL import Connection as __Connection__
try:
    from gevent.socket import wait_read
    from gevent.socket import wait_write
    from gevent.socket import wait_readwrite
except ImportError:
    import select
    def wait_read(fd, timeout):
        return select.select([fd], [], [fd], timeout)
    def wait_write(fd, timeout):
        return select.select([fd], [fd], [fd], timeout)
    def wait_readwrite(fd, timeout):
        return select.select([fd], [fd], [fd], timeout)


class Connection(object):

    def __init__(self, context, sock):
        self._context = context
        self._sock = sock
        self._timeout = sock.gettimeout()
        self._connection = __Connection__(context, sock)

    def __getattr__(self, attr):
        if attr not in ('_context', '_sock', '_timeout', '_connection'):
            return getattr(self._connection, attr)

    def accept(self):
        sock, addr = self._sock.accept()
        client = Connection(sock._context, sock)
        return client, addr

    def do_handshake(self):
        while True:
            try:
                self._connection.do_handshake()
                break
            except (WantReadError, WantX509LookupError, WantWriteError):
                sys.exc_clear()
                wait_readwrite(self._sock.fileno(), timeout=self._timeout)

    def connect(self, *args, **kwargs):
        while True:
            try:
                self._connection.connect(*args, **kwargs)
                break
            except (WantReadError, WantX509LookupError):
                sys.exc_clear()
                wait_read(self._sock.fileno(), timeout=self._timeout)
            except WantWriteError:
                sys.exc_clear()
                wait_write(self._sock.fileno(), timeout=self._timeout)

    def send(self, data, flags=0):
        while True:
            try:
                self._connection.send(data, flags)
                break
            except (WantReadError, WantX509LookupError):
                sys.exc_clear()
                wait_read(self._sock.fileno(), timeout=self._timeout)
            except WantWriteError:
                sys.exc_clear()
                wait_write(self._sock.fileno(), timeout=self._timeout)
            except SysCallError as e:
                if e[0] == -1 and not data:
                    # errors when writing empty strings are expected and can be ignored
                    return 0
                raise

    def recv(self, bufsiz, flags=0):
        pending = self._connection.pending()
        if pending:
            return self._connection.recv(min(pending, bufsiz))
        while True:
            try:
                return self._connection.recv(bufsiz, flags)
            except (WantReadError, WantX509LookupError):
                sys.exc_clear()
                wait_read(self._sock.fileno(), timeout=self._timeout)
            except WantWriteError:
                sys.exc_clear()
                wait_write(self._sock.fileno(), timeout=self._timeout)
            except ZeroReturnError:
                return ''

    def read(self, bufsiz, flags=0):
        return self.recv(bufsiz, flags)

    def write(self, buf, flags=0):
        return self.sendall(buf, flags)
