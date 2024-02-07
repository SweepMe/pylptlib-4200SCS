import logging, sys
from pathlib import Path
from tcp_client.ProxyClass import TCPProxy, PipeProxy, RunServer

logging.basicConfig(stream=sys.stdout)
# remove for production use:
logging.getLogger("ClientProxy").setLevel(logging.DEBUG)

# t = TCPProxy("TargetClass", "127.0.0.1", 8888)
# p = TCPProxy("Param", "127.0.0.1", 8888)


rs = RunServer(42, server_py=Path("main_test.py"))

t = PipeProxy("TargetClass", "sweepmetestpipe")
p = PipeProxy("Param", "sweepmetestpipe")


t.do_something("wonder")

v = t.get_double(p.PARAM2)
print(v)

gate = t.create_complicated_object()
drain = t.create_complicated_object()
source = t.create_complicated_object()
t.set_co(gate, 7)
t.set_co(drain, p.PARAM1)
t.set_co(source, 2)

print(t.get_co(gate))
print(t.get_co(source))
print(t.get_co(drain))

rs.release(42)

print("x")
