import asyncio
import json
import builtins
import traceback
import sys
from typing import Dict, Any, Optional
from tblib import Traceback
import logging


class Server:
    _target_classes: Dict[str, object]
    _local_variables: Dict[str, Any]
    _local_variable_count: int

    def __init__(self, served_objects: Dict[str, Any]):
        self._target_classes = served_objects
        self._local_variable_count = 0
        self._local_variables = {}

    def return_target(self, target_class: str):
        return self._target_classes[target_class]

    def convert_argument_from_json(self, arg):
        if isinstance(arg, list):
            return [self.convert_argument_from_json(element) for element in arg]
        arg_type = arg["type"]
        arg_value = arg["value"]
        if arg_type == "RemoteVar":
            return self._local_variables[str(arg_value)]
        elif arg_type == "NoneType":
            return None
        return getattr(builtins, arg_type)(arg_value)

    def convert_argument_to_json(self, arg):
        # tuples become lists in json anyway, so treat them the same here
        if isinstance(arg, list) or isinstance(arg, tuple):
            return [self.convert_argument_to_json(element) for element in arg]
        arg_type = type(arg).__name__
        # complex types are not transferred but saved locally and only a reference is sent back
        if not hasattr(builtins, arg_type) and arg_type != "NoneType":
            self._local_variable_count += 1
            self._local_variables[str(self._local_variable_count)] = arg
            arg_type = "RemoteVar"
            arg = str(self._local_variable_count)
        return {
            "type": arg_type,
            "value": arg
        }

    def run_command(self, command: str) -> str:
        command_json = json.loads(command)
        if "function" not in command_json:
            return self.get_attribute(command)
        target_class = command_json["class"]
        function = command_json["function"]
        args_raw = command_json.get("args", [])
        args = [self.convert_argument_from_json(arg) for arg in args_raw]
        kwargs_raw = command_json.get("kwargs", {})
        kwargs = {k: self.convert_argument_from_json(v) for k, v in kwargs_raw.items()}
        target_function = getattr(self.return_target(target_class), function)
        result = target_function(*args, **kwargs)
        ret = self.convert_argument_to_json(result)
        return json.dumps({
            "status": "success",
            "return": ret
        })

    def get_attribute(self, command: str) -> str:
        command_json = json.loads(command)
        target_class = command_json["class"]
        attribute = command_json["attribute"]
        target_attribute = getattr(self.return_target(target_class), attribute)
        if callable(target_attribute):
            ret = {
                "type": "callable",
                "value": None
            }
        else:
            ret = self.convert_argument_to_json(target_attribute)
        return json.dumps({
            "status": "success",
            "return": ret
        })


server: Optional[Server] = None


async def handle_request(reader, writer):

    try:
        data = await reader.readline()
        command = data.decode("utf-8")
        result = server.run_command(command)
        result = result.encode("utf-8")
    except Exception as e:
        traceback.print_exc()
        et, ev, tb = sys.exc_info()
        message = repr(ev)
        tb = Traceback(tb).to_dict()
        result = json.dumps(
            {
                "status": "exception",
                "message": message,
                "traceback": tb
            }
        ).encode("utf-8")
    writer.write(result + b'\n')
    await writer.drain()

    writer.close()


async def main(local_ip: str, local_port: int):
    tcp_server = await asyncio.start_server(
        handle_request, local_ip, local_port)

    addr = tcp_server.sockets[0].getsockname()
    logging.info(f'Serving on {addr}')

    async with tcp_server:
        await tcp_server.serve_forever()


def run_server(local_ip: str, local_port: int, served_objects: Dict[str, Any]):
    global server
    if server is not None:
        raise Exception("The server cannot be run more than once.")
    server = Server(served_objects)
    asyncio.run(main(local_ip, local_port))
