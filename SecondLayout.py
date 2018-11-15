from __future__ import print_function, unicode_literals

import logging
logger = logging.getLogger(__name__)

import os.path
import sys
import getopt
import signal
import locale
import gettext
import ctypes
import tempfile

from pympress import util

if util.IS_WINDOWS:
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang

locale.setlocale(locale.LC_ALL, '')
gettext.install('pympress', util.get_locale_dir())

# Catch all uncaught exceptions in the log file:
def uncaught_handler(*exc_info):
    logger.critical('Uncaught exception:\n{}'.format(logging.Formatter().formatException(exc_info)))
    sys.__excepthook__(*exc_info)

sys.excepthook = uncaught_handler

def usage():
    print(_("Usage: {} [options] <presentation_file>").format(sys.argv[0]))
    print("")
    print(_("Options:"))
    print("    -h, --help                       " + _("This help"))
    print("    -t mm[:ss], --talk-time=mm[:ss]  " + _("The estimated (intended) talk time in minutes"))
    print("                                       " + _("(and optionally seconds)"))
    print("    --log=level:                     " + _("Set level of verbosity in log file:"))
    print("                                       " + _("{}, {}, {}, {}, or {}").format("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"))
    print("")

def main(argv = sys.argv[1:]):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        opts, args = getopt.getopt(argv, "ht:", ["help", "talk-time=", "log="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    ett = 0
    log_level = logging.ERROR

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-t", "--talk-time"):
            t = ["0" + n.strip() for n in arg.split(':')]
            try:
                m = int(t[0])
                s = int(t[1])
            except ValueError:
                print(_("Invalid time (mm or mm:ss expected), got \"{}\"").format(text))
                usage()
                sys.exit(2)
            except IndexError:
                s = 0
            ett = m * 60 + s
        elif opt == "--log":
            numeric_level = getattr(logging, arg.upper(), None)
            if isinstance(numeric_level, int):
                log_level = numeric_level
            else:
                print(_("Invalid log level \"{}\", try one of {}").format(
                    arg, "DEBUG, INFO, WARNING, ERROR, CRITICAL"
                ))

    logging.basicConfig(filename=os.path.join(tempfile.gettempdir(), 'pympress.log'), level=log_level)

    pympress_meta = util.get_pympress_meta()
    logger.info('\n  '.join(['Pympress version {} by:'.format(pympress_meta.__version__)] + pympress_meta.__copyright__.split('\n')))

    # PDF file to open passed on command line?
    name = os.path.abspath(args[0]) if len(args) > 0 else None

    # Create windows
    from pympress import ui
    gui = ui.UI(ett, name)
    gui.run()


if __name__ == "__main__":
    main()