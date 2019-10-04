import os
import sys

from .version import get_cli_version

MOHAND_ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
MOHAND_VENDOR = os.sep.join([MOHAND_ROOT, "vendor"])
# Inject vendored directory into system path.
sys.path.insert(0, MOHAND_VENDOR)

__version__ = get_cli_version()
