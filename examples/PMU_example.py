import time

# Option1: when script runs on the 4200-SCS
from pylptlib import lpt, param

# Option2: when script runs on an external measurement computer
# from ProxyClass import TCPProxy
# tcp_ip = "192.168.0.4"
# lpt = TCPProxy("lpt", tcp_ip, 8888)
# param = TCPProxy("param", tcp_ip, 8888)

lpt.initialize()
lpt.tstsel(1)
lpt.devint()
lpt.dev_abort()

# maximum time to wait until pulse sweep has finished
timeout = 30
channel = 1

card_id = lpt.getinstid("PMU1")
print("Pulse card id:", card_id)

channels = [1, 2]

for channel in channels:

    lpt.rpm_config(
        card_id,
        channel,
        modifier=param.KI_RPM_PATHWAY,
        value=param.KI_RPM_PULSE,
    )

    lpt.pulse_meas_sm(
        card_id,
        channel,
        acquire_type=0,
        acquire_meas_v_ampl=1,
        acquire_meas_v_base=0,
        acquire_meas_i_ampl=1,
        acquire_meas_i_base=0,
        acquire_time_stamp=1,
        llecomp=0,
    )

    lpt.pulse_ranges(
        card_id,
        channel,
        v_src_range=10.0,
        v_range_type=0,
        v_range=10.0,
        i_range_type=0,
        i_range=0.2,
    )

    lpt.pulse_limits(card_id, channel, v_limit=5.0, i_limit=1.0, power_limit=10.0)

    lpt.pulse_meas_timing(
        card_id,
        channel,
        start_percent=0.2,
        stop_percent=0.8,
        num_pulses=4,
    )

    lpt.pulse_source_timing(
        card_id,
        channel,
        period=20e-6,
        delay=1e-7,
        width=10e-6,
        rise=1e-7,
        fall=1e-7,
    )

    lpt.pulse_load(
        card_id,
        channel,
        load=1e6,
    )

    lpt.pulse_sweep_linear(card_id,
                           channel,
                           sweep_type=param.PULSE_AMPLITUDE_SP,
                           start=1.0,
                           stop=2.0,
                           step=0.1)

    lpt.pulse_output(card_id, channel, out_state=1)

lpt.pulse_exec(mode=1)

while True:
    time.sleep(0.1)
    status, elapsed_time = lpt.pulse_exec_status()
    print("Execution status:", status, "Time elapsed:", elapsed_time)

    if status != param.PMU_TEST_STATUS_RUNNING:
        break
    if elapsed_time > timeout:
        lpt.dev_abort()

for channel in channels:

    print()

    buffer_size = lpt.pulse_chan_status(
        card_id,
        channel,
    )

    print("Buffer size", str(channel) + ":", buffer_size)

    # fetch results
    v_meas, i_meas, timestamp, statuses = lpt.pulse_fetch(
        card_id,
        channel,
        start_index=0,
        stop_index=buffer_size - 1  # because index starts from 0 
    )

    decoded_status = [lpt.decode_pulse_status(status) for status in statuses]

    print("Status:", statuses)
    print("Status interpreted:", decoded_status)
    print("Timestamps:", timestamp)
    print("Voltages:", v_meas)
    print("Currents:", i_meas)

for channel in channels:

    lpt.pulse_output(card_id, channel, out_state=0)

lpt.devint()
lpt.tstdsl()
