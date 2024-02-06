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

# run_server(served_objects, local_ip="127.0.0.1", local_port=8888)
run_server(served_objects, pipe_name="sweepmetestpipe")
