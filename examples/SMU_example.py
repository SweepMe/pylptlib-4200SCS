import time

# Option1: when script runs on the 4200-SCS
from pylptlib import lpt
from pylptlib import param

# Option2: when script runs on an external measurement computer
# from ProxyClass import Proxy
# tcp_ip = "192.168.0.4"
# lpt = Proxy(tcp_ip, 8888, "lpt")
# param = Proxy(tcp_ip, 8888, "param")

lpt.initialize()
lpt.tstsel(1)
lpt.devint()

card_id = lpt.getinstid("SMU1")

print("SMU card id:", card_id)

lpt.setmode(card_id, param.KI_INTGPLC, 0.01)

lpt.forcev(card_id, 0.0)

starttime = time.time()

num_readings = 10

for _ in range(num_readings ):
    current = lpt.intgi(card_id)
    print("Current", current)

duration = time.time() - starttime

print()
print("Total time in s:", duration)
print("Time per point in s:", duration / num_readings)

lpt.forcev(card_id, 0.0)

lpt.devint()
lpt.tstdsl()
