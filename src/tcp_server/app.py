import sys
import logging
from server import run_server

# import LPT library functions
from pylptlib import lpt

# import LPT library instrument IDs
# from pylptlib import inst

# import LPT library parameter constants
from pylptlib import param


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

served_objects = {
    "lpt": lpt,
    # "inst": inst,
    "param": param,
}

# localhost server, e.g. if running the client on the 4200-SCS
# run_server("127.0.0.1", 8888, served_objects)

# server if running the client on an external computer
run_server("127.0.0.1", 8888, served_objects)
