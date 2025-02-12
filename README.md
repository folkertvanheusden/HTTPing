httping
=======

Ping with HTTP requests, see <http://www.vanheusden.com/httping/>.

Compiling:

* `cmake -B build`
* `cmake --build build`

This configuration will build a binary with the minimal functionality.
You can use the following options to add more features to httping:

If you need the SSL support, use (requires `OpenSSL` library):

* `cmake -DUSE_SSL=ON build`

If you would like the TUI (text user interface) to be included (for -K),
use (requires `ncurses` library):

* `cmake -DUSE_TUI=ON build`

Adding `-DUSE_FFTW3=ON` to the `-DUSE_TUI=ON` allows TUI to show performance graphics. This option requires `fftw3` library.

If you want httping to use local translations, add `-DUSE_GETTEXT=ON` to
the cmake commandline.

The AGPL v3.0 license applies to this software.
