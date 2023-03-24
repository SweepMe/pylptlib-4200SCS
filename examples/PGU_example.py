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

card_id = lpt.getinstid("PMU1")  # OR VPU1
print("K4200 card id:", card_id)

# setup pulses/waveform
lpt.pg2_init(card_id, mode_id=0)  # set to standard pulse
lpt.pulse_init(card_id)  # reset standard pulse settings to default
lpt.pulse_trig_source(card_id, source=0)

channels = [1, 2]

for channel in channels:

    pulse_period_s = 5e-6 * channel  # s
    pulse_width_s = 2e-6 * channel  # s
    pulse_delay_s = 1e-6 * channel  # s
    pulse_high_v = 1.2
    pulse_low_v = -0.2
    dut_load = 1e6  # Ohm
    pulse_count = 10
    rise_time = 100e-9
    fall_time = 100e-9

    lpt.rpm_config(card_id, channel, param.KI_RPM_PATHWAY, param.KI_RPM_PULSE)

    lpt.pulse_load(card_id, channel, dut_load)

    lpt.pulse_range(
        card_id,
        channel,
        5.0,  # range
    )

    lpt.pulse_delay(card_id, channel, pulse_delay_s)
    lpt.pulse_period(card_id, channel, pulse_period_s)
    lpt.pulse_width(card_id, channel, pulse_width_s)
    lpt.pulse_rise(card_id, channel, rise_time)
    lpt.pulse_fall(card_id, channel, fall_time)
    lpt.pulse_vhigh(card_id, channel, pulse_high_v)
    lpt.pulse_vlow(card_id, channel, pulse_low_v)

    # triggers the pulse output
    pulse_modes = {"Burst": 0, "Continuous": 1, "Trigger burst": 2}
    mode = pulse_modes["Continuous"]
    lpt.pulse_trig(card_id, mode)

for channel in channels:
    lpt.pulse_output(card_id, channel, 1)

# applies pulse for 3 seconds
time.sleep(3)

for channel in channels:
    lpt.pulse_output(card_id, channel, 0)

lpt.devint()
lpt.tstdsl()
