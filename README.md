httping
=======

Ping with HTTP requests, see <http://www.vanheusden.com/httping/>.

Compiling:

* cmake -B build
* cmake --build build

If you would like the TUI (text user interface) to be included (for -K),
use:

* cmake -DUSE_TUI=ON build

If you want httping to use local translations, add "-DUSE_GETTEXT=ON" to
the cmake commandline.

The AGPL v3.0 license applies to this software.
