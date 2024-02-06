import sys
import logging
import traceback
from configparser import ConfigParser
from pathlib import Path

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


def get_parent_folder() -> Path:
    if getattr(sys, 'frozen', False):
        # in case of pyinstaller exe
        return Path(sys.executable).parent
    # in case of python script
    return Path(__file__).parent


try:
    config_file = get_parent_folder() / "4200-Server.ini"
    if not config_file.is_file():
        msg = f"The file {config_file!s} could not be found."
        raise FileNotFoundError(msg)

    config = ConfigParser()
    config.read(config_file)

    ip = config["server"]["IP"]
    port = config["server"]["Port"]
    auth = config["server"].get("RequireAuthentication", "")
    if auth.lower() != "false":
        msg = ("Authentication is not supported yet. You need to set `RequireAuthentication = false` "
               "in the configuration file.")
        raise NotImplementedError(msg)

    run_server(served_objects, local_ip=ip, local_port=int(port))
except Exception:
    traceback.print_exc()
    import msvcrt
    print("Press any key to continue...")
    msvcrt.getch()
