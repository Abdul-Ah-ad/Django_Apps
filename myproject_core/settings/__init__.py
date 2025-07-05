from myproject_core.settings.base import *

try:
    from myproject_core.settings.local import *
except ImportError:
    raise ImportError("You need to create a local.py settings file from sample.local.py")

