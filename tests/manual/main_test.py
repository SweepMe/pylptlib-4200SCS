import sys
import logging
from tcp_server.server import run_server

import test_libs.library as lpt
import test_libs.parameters as param

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

served_objects = {
            "TargetClass": lpt,
            "Param": param
        }

run_server("127.0.0.1", 8888, served_objects)
