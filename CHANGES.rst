============
 Change Log
============
All notable changes to this project will be documented in this file.

Version 1.2
===========

Added
-----
- Added timeout test
- Added server test and moved tests to their own subdirectory
- Added COPYING

Fixed
-----
- Fix infinite loop in __iowait (#6)
- Removed unnecessary guard from __getattr__
- Fixed incorrect attribute used in accept()
- Be more direct about the Connection class used in accept()
- sendall and shutdown will no longer block the process (now use
  __iowait)
- Removed read, write, close and makefile methods from
  Connection. These aren't part of pyOpenSSL's Connection API so
  shouldn't be here either.
- Correct the description of how gevent_openssl works in README
