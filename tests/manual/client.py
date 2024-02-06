import logging, sys
from tcp_client.ProxyClass import TCPProxy, PipeProxy

logging.basicConfig(stream=sys.stdout)
# remove for production use:
logging.getLogger("TCPClientProxy").setLevel(logging.DEBUG)

# t = TCPProxy("TargetClass", "127.0.0.1", 8888)
# p = TCPProxy("Param", "127.0.0.1", 8888)

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

print("x")
