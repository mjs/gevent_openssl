=============
gevent-openssl
=============

This library wraps pyOpenSSL to make it compatible with gevent. OpenSSL connection
operations that would normally block the current thread will only block the
current greenlet instead.

Requirements
------------

* PyOpenSSL >= 0.11
* gevent (compatible with 1.0 pre-releases as well)


Usage
-----

Instead of importing OpenSSL directly, do so in the following manner:

..
    
    import gevent_openssl as OpenSSL
    
or

..
    
    import gevent_openssl; gevent_openssl.monkey_patch()



Any calls that would have blocked the current thread will now only block the
current green thread.


About
-----

This compatibility is accomplished by ensuring the nonblocking flag is set
before any blocking operation and the OpenSSL Connection is polled internally
to trigger needed events.

License
-------
New BSD
