==============
gevent-openssl
==============
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
This compatibility is accomplished by yielding to the gevent scheduler
when pyOpenSSL is waiting to be able to read or write data.

License
-------
New BSD

History
-------
This project was originally created by Phus Lu (phus.lu@gmail.com) and
is now maintained by Menno Finlay-Smits (menno@freshfoo.com).
