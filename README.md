httping
=======

Ping with HTTP requests, see http://www.vanheusden.com/httping/


Compiling:

* mkdir build
* cd build
* cmake ..
* make

If you would like the TUI (text user interface) to be included (for -K),
use:
* cmake -DUSE_TUI=1 ..

If you want httping to use local translations, add "-DUSE_GETTEXT=1" to
the cmake commandline.
