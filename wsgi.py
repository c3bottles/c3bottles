#!/usr/bin/env python3

# To be able to import modules in the project root directory, that directory
# has to be added to the module search path if it is not the working directory.
# This especially confuses Apache. If you are experiencing problems with modules
# not being found, please uncomment the following lines:

# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from c3bottles import c3bottles
from c3bottles.lib.metrics import monitor

application = c3bottles

if c3bottles.config.get("PROMETHEUS_ENABLED", False):
    monitor(c3bottles)
