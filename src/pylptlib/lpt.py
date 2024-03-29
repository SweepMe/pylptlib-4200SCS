# MIT License

# Copyright (c) 2023 SweepMe! GmbH (sweep-me.net)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ctypes as c
from typing import List, Tuple

from .error_codes import ERROR_CODES

_dll_path = r"C:\s4200\sys\bin\lptlib.dll"
_dll = None

DEBUG_MODE = True

# ### UTILITY FUNCTIONS


class K4200Error(Exception):
    """wrapped error"""


def make_char_pointer(string: str):
    """make a char pointer from a python string
    to be used without c.byref"""
    bytes_ = string.encode("ascii")
    return c.c_char_p(bytes_)


def make_generic_array(len_: int, values_list: list = None, data_type=c.c_double):
    """makes a c_array of data_types. The array values are 0 if no values_list is specified
    if values is not empty a length len_ is to be given
    """
    if values_list:
        if not len_:
            len_ = len(values_list)
        return (data_type * int(len_))(*values_list)
    else:
        return (data_type * int(len_))()


def make_double_array(len_: int, values: list = None):
    """makes a c_double array. The array values are 0 if no values list is specified
    - if values is not empty a length len_ is to be specified
    """
    return make_generic_array(len_, values, c.c_double)


def make_double_array_pointer(len_: int, values: list = None):
    """ make a pointer to an c_double array
    values = [] makes an empty array pointer"""
    if values:
        array = (c.c_double * int(len_))(*values)
    else:
        array = (c.c_double * int(len_))()
    return c.cast(array, c.POINTER(c.c_double))


def make_int_array_pointer(len_: int, values: list = None):
    """ make array pointer to a c_int array
    The array values are 0 if no values list is specified
    - if values is not empty please a length len_ is to be specifiedr"""

    array = make_generic_array(len_, values, data_type=c.c_int32)
    return c.cast(array, c.POINTER(c.c_int32))


def create_string_buffer(string: str, size=128):
    """make a char bufferr from a python string
   to be used with c.byref"""
    return c.create_string_buffer(string.encode("ascii"), size=size)


def set_library_path(path):
    """ change the library default path"""
    global _dll_path
    _dll_path = path


def check_error(error_code: c.c_int32, *args):
    """ get the error codes if there was an error
    There is some unclear Keithley magic with filling the place holders available for some
     error codes."""

    error_code = int(error_code)
    if error_code == 0:
        return

    if DEBUG_MODE:
        print("error #: ", error_code)

    error_string = ERROR_CODES[error_code]

    if DEBUG_MODE:
        print("error message: ", error_string)

    place_holders = error_string.count("%")
    if len(args) == place_holders:
        raise K4200Error(error_string % args)
    else:
        raise K4200Error(error_string)


def initialize():
    """ load the library with ctypes"""
    global _dll
    _dll = c.WinDLL(_dll_path)


# ### GENERAL FUNCTIONS


def tstsel(id_: int):
    """select test station"""

    err = _dll.tstsel(c.c_int32(id_))  # equiv to c_long
    check_error(err)


def tstdsl():
    """deselect test station"""
    err = _dll.tstdsl()
    check_error(err)


def devint():
    """ reset all active instruments in the system to their default states. """
    err = _dll.devint()
    check_error(err)


def getinstid(id_string: str):
    """return the id for a desired card"""
    chars_p = make_char_pointer(id_string)
    c_instr_id = c.c_int32()
    err = _dll.getinstid(chars_p, c.byref(c_instr_id))
    check_error(err)
    return int(c_instr_id.value)


def setmode(instr_id: int, param: int, value):

    err = _dll.setmode(c.c_int32(instr_id), c.c_long(param), c.c_double(value))
    check_error(err)


# ### SMU commands


def forcev(instr_id: int, value: float):
    """program a sourcing instrument to generate a voltage at a specific level"""
    err = _dll.forcev(c.c_int32(instr_id), c.c_double(value))
    check_error(err)


def forcei(instr_id: int, value: float):
    """program a sourcing instrument to generate a current at a specific level"""
    err = _dll.forcei(c.c_int32(instr_id), c.c_double(value))
    check_error(err)


def intgv(instr_id: int) -> float:
    """measure current"""
    meas_value = c.c_double()
    err = _dll.intgv(c.c_int32(instr_id), c.byref(meas_value))
    check_error(err)
    return float(meas_value.value)


def intgi(instr_id: int) -> float:
    """measure current"""
    meas_value = c.c_double()
    err = _dll.intgi(c.c_int32(instr_id), c.byref(meas_value))
    check_error(err)
    return float(meas_value.value)


def limitv(instr_id: int, limit_val: float):
    """set current limit"""
    err = _dll.limitv(c.c_int32(instr_id), c.c_double(limit_val))
    check_error(err)


def limiti(instr_id: int, limit_val: float):
    """set voltage limit"""
    err = _dll.limiti(c.c_int32(instr_id), c.c_double(limit_val))
    check_error(err)


def lorangev(instr_id: int, range: float):
    """define the bottom voltage autorange limit"""
    # Argument 'range' shadows the built-in function 'range' which is ok
    # here as no further processing is done within the local scope of the function
    err = _dll.lorangev(c.c_int32(instr_id), c.c_double(range))
    check_error(err)


def lorangei(instr_id: int, range: float):
    """define the bottom current autorange limit"""
    # Argument 'range' shadows the built-in function 'range' which is ok
    # here as no further processing is done within the local scope of the function
    err = _dll.lorangei(c.c_int32(instr_id), c.c_double(range))
    check_error(err)


def measi(instr_id: int):
    c_instr_id = c.c_int32(instr_id)
    meas_result = c.c_double()
    err = _dll.measi(c_instr_id, c.byref(meas_result))
    check_error(err)
    return float(meas_result.value)


def measv(instr_id: int):
    c_instr_id = c.c_int32(instr_id)
    meas_result = c.c_double()
    err = _dll.measv(c_instr_id, c.byref(meas_result))
    check_error(err)
    return float(meas_result.value)


def meast(instr_id: int):
    c_instr_id = c.c_int32(instr_id)
    meas_result = c.c_double()
    err = _dll.meast(c_instr_id, c.byref(meas_result))
    check_error(err)
    return float(meas_result.value)


def rangev(instr_id: int, range: float):
    """select a voltage range and prevent the selected instrument from autoranging.
    """
    # Argument 'range' shadows the built-in function 'range' which is ok
    # here as no further processing is done within the local scope of the function
    err = _dll.rangev(c.c_int32(instr_id), c.c_double(range))
    check_error(err)


def rangei(instr_id: int, range: float):
    """select a current range and prevent the selected instrument from autoranging."""
    # Argument 'range' shadows the built-in function 'range' which is ok
    # here as no further processing is done within the local scope of the function
    err = _dll.rangei(c.c_int32(instr_id), c.c_double(range))
    check_error(err)


def setauto(instr_id: int):
    """re-enable autoranging and cancel any previous rangeX command for the specified instrument"""
    err = _dll.setauto(c.c_int32(instr_id))
    check_error(err)


# ### PG2


def arb_array(instr_id: int, chan: int, time_per_pt: float, length: int, level_arr: list,
              fname: str):
    """ define a full arb waveform and name the file"""

    voltages_array_p = make_double_array_pointer(len(level_arr), level_arr)
    len_c = c.c_int32(length)
    c_name_p = make_char_pointer(fname)

    err = _dll.arb_array(c.c_int32(instr_id), c.c_int32(chan), c.c_double(time_per_pt), len_c,
                         voltages_array_p, c_name_p)
    check_error(err)


def arb_file(instr_id: int, chan: int, fname: str):
    """ load a waveform from an existing full arb waveform file"""

    c_name_p = make_char_pointer(fname)

    err = _dll.arb_file(c.c_int32(instr_id), c.c_int32(chan), c_name_p)
    check_error(err)


def getstatus(instr_id: int, parameter: int):

    result = c.c_double()

    err = _dll.getstatus(c.c_int32(instr_id), c.c_int32(parameter), c.byref(result))
    check_error(err)

    return float(result.value)


def pg2_init(instr_id: int, mode_id: int):
    """ reset the pulse card to specified pulse mode & mode defaults
    mode ids: 0 -> standard, 1: segment arb 2: full arb    """

    err = _dll.pg2_init(c.c_int32(instr_id), c.c_int32(mode_id))
    check_error(err)


def pulse_burst_count(instr_id: int, chan: int, count: int):
    """set the number of pulses to output during a burst sequence"""

    err = _dll.pulse_burst_count(
        c.c_int32(instr_id),
        c.c_int32(chan),
        c.c_uint32(count)  # manual wants unsigned!
    )
    check_error(err)


def pulse_current_limit(instr_id: int, chan: int, ilimit: float):
    """set the current limit for the pulse card"""
    err = _dll.pulse_current_limit(c.c_int32(instr_id), c.c_int32(chan), c.c_double(ilimit))
    check_error(err)


def pulse_dc_output(instr_id: int, chan: int, dcvalue: float):
    """select dc output mode and set voltage level
    WARNING: this sets the channel voltage value when it is turned on (using pulse_output).
     If the output is already enabled, the voltage level change is immediate, before the pulsing is
     started with a pulse_trig command."""

    err = _dll.pulse_dc_output(c.c_int32(instr_id), c.c_int32(chan), c.c_double(dcvalue))
    check_error(err)


def pulse_delay(instr_id: int, chan: int, delay: float):
    """set s the delay time from the trigger to when the pulse output starts"""

    err = _dll.pulse_delay(c.c_int32(instr_id), c.c_int32(chan), c.c_double(delay))
    check_error(err)


def pulse_fall(instr_id: int, chan: int, fallt: float):
    """set the fall transition time for the pulse output"""

    err = _dll.pulse_fall(c.c_int32(instr_id), c.c_int32(chan), c.c_double(fallt))
    check_error(err)


def pulse_halt(instr_id: int):
    """stop all pulse output from the pulse card"""

    err = _dll.pulse_halt(c.c_int32(instr_id))
    check_error(err)


def pulse_init(instr_id: int):
    """reset card to defaults of currently selected pulse mode"""
    err = _dll.pulse_init(c.c_int32(instr_id))
    check_error(err)


def pulse_load(instr_id: int, chan: int, load: float):
    """sets the output impedance for the DUT load"""

    err = _dll.pulse_load(c.c_int32(instr_id), c.c_int32(chan), c.c_double(load))

    check_error(err)


def pulse_output(instr_id: int, chan: int, out_state: bool):
    """ sets pulse card output to on or off"""
    err = _dll.pulse_output(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(out_state))
    check_error(err)


def pulse_output_mode(instr_id: int, chan: int, mode: int):
    """ set the output mode to NORMAL (0) or COMPLEMENT (1)
    For complement the high and low levels are swapped"""
    err = _dll.pulse_output_mode(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(mode))
    check_error(err)


def pulse_period(instr_id: int, period: float):
    """ pulse period in s """

    err = _dll.pulse_period(c.c_int32(instr_id), c.c_double(period))
    check_error(err)


def pulse_range(instr_id: int, chan: int, range: float):
    """sets the voltage range for low v (fast speed)/ high v (low speed)
    v_range = 5 or 20"""
    # Argument 'range' shadows the built-in function 'range' which is ok
    # here as no further processing is done within the local scope of the function
    err = _dll.pulse_range(c.c_int32(instr_id), c.c_int32(chan), c.c_double(range))
    check_error(err)


def pulse_rise(instr_id: int, chan: int, riset: float):
    """set the rise transition time for the pulse """
    err = _dll.pulse_rise(c.c_int32(instr_id), c.c_int32(chan), c.c_double(riset))

    check_error(err)


def pulse_ssrc(instr_id: int, chan: int, state: bool, ctrl: int):
    """set the high-endurance output relay (HEOR) for the PGU channel.
        control_mode (ctrl): 0 -> auto, 1 -> manual (state), 3 -> trig out """
    err = _dll.pulse_ssrc(
        c.c_int32(instr_id),
        c.c_int32(chan),
        c.c_int32(state),
        c.c_int32(ctrl),
    )
    check_error(err)


def pulse_trig(instr_id: int, mode: int):
    """set the trigger mode for the pulse output"""
    err = _dll.pulse_trig(
        c.c_int32(instr_id),
        c.c_int32(mode),
    )
    check_error(err)


def pulse_trig_output(instr_id: int, state: bool):
    """set the output trigger on or off."""
    err = _dll.pulse_trig_output(
        c.c_int32(instr_id),
        c.c_int32(state),
    )
    check_error(err)


def pulse_trig_polarity(instr_id: int, polarity: int):
    """set the polarity of the outpiut trig card"""
    err = _dll.pulse_trig_polarity(
        c.c_int32(instr_id),
        c.c_int32(polarity),
    )
    check_error(err)


def pulse_trig_source(instr_id: int, source: int):
    """set trigger source
        0: software
        1: ext rising (initial only)
        2: ext falling (initial only)
        3: ext rising (per pulse)
        4: ext falling (per pulse)
        5: internal trig bus
    """
    err = _dll.pulse_trig_source(
        c.c_int32(instr_id),
        c.c_int32(source),
    )
    check_error(err)


def pulse_vhigh(instr_id: int, chan: int, vhigh: float):
    """  set the pulse voltage high level
    WARNING: this sets the channel voltage value when it is turned on (using pulse_output).
     If the output is already enabled, the voltage level change is immediate, before the pulsing is
     started with a pulse_trig command."""
    err = _dll.pulse_vhigh(c.c_int32(instr_id), c.c_int32(chan), c.c_double(vhigh))
    check_error(err)


def pulse_vlow(instr_id: int, chan: int, vlow: float):
    """  set the pulse voltage low level
    WARNING: this sets the channel voltage value when it is turned on (using pulse_output).
     If the output is already enabled, the voltage level change is immediate, before the pulsing is
     started with a pulse_trig command."""
    err = _dll.pulse_vlow(c.c_int32(instr_id), c.c_int32(chan), c.c_double(vlow))
    check_error(err)


def pulse_width(instr_id: int, chan: int, width: float):
    """aset the output pulse width in s"""
    err = _dll.pulse_width(c.c_int32(instr_id), c.c_int32(chan), c.c_double(width))
    check_error(err)


def seg_arb_define(instr_id: int, chan: int, nsegments: int, startvals: list, stopvals: list,
                   timevals: list, triggervals: list, output_relay_vals: list):

    start_values_p = make_double_array_pointer(startvals)
    stop_values_p = make_double_array_pointer(stopvals)
    time_values_p = make_double_array_pointer(timevals)
    trig_values_p = make_int_array_pointer(triggervals)
    outp_relay_values_p = make_int_array_pointer(output_relay_vals)

    err = _dll.seg_arb_define(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(nsegments),
                              start_values_p, stop_values_p, time_values_p, trig_values_p,
                              outp_relay_values_p)
    check_error(err)


def seg_arb_file(instr_id: int, chan: int, fname: str):

    fname_c_p = make_char_pointer(fname)
    err = _dll.seg_arb_file(c.c_int32(instr_id), c.c_int32(chan), fname_c_p)
    check_error(err)


# ### PULSE


def dev_abort():
    """ abort a pulse started with pulse exec (non-blocking). NB no card ID
    """
    err = _dll.dev_abort()
    check_error(err)


def pmu_offset_current_comp(instr_id: int):
    """ used to collect offset current constants from the 4225-PMU. The offset
     (open) correction readings are stored in a local file. """

    err = _dll.pmu_offset_current_comp(c.c_int32(instr_id))
    check_error(err)


def pulse_chan_status(instr_id: int, chan: int) -> int:
    """determine how many readings are stored in the data buffer"""

    buffersize = c.c_int32()
    err = _dll.pulse_chan_status(c.c_int32(instr_id), c.c_int32(chan), c.byref(buffersize))
    check_error(err)

    return int(buffersize.value)


def pulse_conncomp(instr_id: int, chan: int, type: int, index: int):
    """ enable/disable compensation
        - type : 1 short, 2 delay
        - index: 0: Disabled, 1: default, 2: default with PMU and RPM 3: custom
    """
    # Argument 'type' shadows the built-in function 'type' which is ok
    # here as no further processing is done within the local scope of the function
    err = _dll.pulse_conncomp(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(type),
                              c.c_int32(index))
    check_error(err)


def pulse_exec(mode: bool) -> int:
    """ execute a pulse in basic/advanced mode"""

    err = _dll.pulse_exec(c.c_int32(mode))
    check_error(err)


def pulse_exec_status() -> Tuple[int, float]:
    """ to check the pulse status during a while pulse exec loop"""
    elapsed_time = c.c_double()
    status = _dll.pulse_exec_status(c.byref(elapsed_time))
    return int(status), float(elapsed_time.value)


def pulse_fetch(instr_id: int, chan: int, start_index: int,
                stop_index: int) -> Tuple[dict, float, float, float]:
    """This command retrieves enabled test data and temporarily stores it in the data buffer

     When using pulse_fetch to retrieve data, you need to pause the program to allow time for the
     buffer to fill. You can use the sleep command to pause for a specified time, or you can use the
     pulse_exec_status command in a while loop to wait until the test is completed.

     indices as in python: for 50 use 0 and 49
    """

    buffer_size = stop_index - start_index + 1

    meas_v = make_double_array(buffer_size)
    meas_i = make_double_array(buffer_size)
    statuses = make_generic_array(buffer_size, data_type=c.c_ulong())
    timestamp = make_double_array(buffer_size)

    # TODO: check whether statuses needs byref
    err = _dll.pulse_fetch(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(start_index),
                           c.c_int32(stop_index), c.byref(meas_v), c.byref(meas_i),
                           c.byref(timestamp), c.byref(statuses))

    if DEBUG_MODE:
        print("Statuses or error from fetch:", err)
    check_error(err)

    statuses = list(statuses)
    # statuses = [decode_pulse_status(status_bits) for status_bits in statuses]

    if DEBUG_MODE:
        print("Status:", statuses)

    meas_v = [meas_v[i] for i in range(buffer_size)]
    meas_i = [meas_i[i] for i in range(buffer_size)]
    timestamp = [timestamp[i] for i in range(buffer_size)]

    return meas_v, meas_i, timestamp, statuses


def pulse_float(instr_id: int, chan: int, state: bool):
    """set the state of the floating relay for the given pulse instrument.
    """

    err = _dll.pulse_float(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(state))
    check_error(err)


def pulse_limits(instr_id: int, chan: int, v_limit: float, i_limit: float, power_limit: float):
    """ sets the pulse measure I/V limits
    """
    v_limit = c.c_double(v_limit) if v_limit else None
    i_limit = c.c_double(i_limit) if i_limit else None
    power_limit = c.c_double(power_limit) if power_limit else None

    err = _dll.pulse_limits(c.c_int32(instr_id), c.c_int32(chan), v_limit, i_limit, power_limit)
    check_error(err)


def pulse_meas_sm(instr_id: int, chan: int, acquire_type: int, acquire_meas_v_ampl: bool,
                  acquire_meas_v_base: bool, acquire_meas_i_ampl: bool, acquire_meas_i_base: bool,
                  acquire_time_stamp: bool, llecomp: bool):
    """ configures spot mean measurement. See lpt docu.
    Params:
        acquire_type: 0=discrete, 1=average
    """

    acquire_type = c.c_int32(acquire_type)
    chan = c.c_int32(chan)
    acquire_meas_v_ampl = c.c_int32(acquire_meas_v_ampl)
    acquire_meas_v_base = c.c_int32(acquire_meas_v_base)
    acquire_meas_i_ampl = c.c_int32(acquire_meas_i_ampl)
    acquire_meas_i_base = c.c_int32(acquire_meas_i_base)
    acquire_time_stamp = c.c_int32(acquire_time_stamp)
    load_line_effect_comp = c.c_int32(llecomp)

    err = _dll.pulse_meas_sm(c.c_int32(instr_id), chan, acquire_type, acquire_meas_v_ampl,
                             acquire_meas_v_base, acquire_meas_i_ampl, acquire_meas_i_base,
                             acquire_time_stamp, load_line_effect_comp)
    check_error(err)


def pulse_meas_timing(instr_id: int, chan: int, start_percent: float, stop_percent: float,
                      num_pulses: int):
    """ set the measurements windows. see lpt manual
    """

    err = _dll.pulse_meas_timing(c.c_int32(instr_id), c.c_int32(chan), c.c_double(start_percent),
                                 c.c_double(stop_percent), c.c_int32(num_pulses))
    check_error(err)


def pulse_meas_wfm(instr_id: int, chan: int, acquire_type: bool, acquire_meas_v: bool,
                   acquire_meas_i: bool, acquire_time_stamp: bool, llecomp: bool):
    """ configures waveform measurements """

    acquire_type = c.c_int32(acquire_type)
    acquire_meas_V = c.c_int32(acquire_meas_v)
    acquire_meas_I = c.c_int32(acquire_meas_i)
    acquire_time_stamp = c.c_int32(acquire_time_stamp)
    load_line_effect_comp = c.c_int32(llecomp)

    err = _dll.pulse_meas_wfm(
        c.c_int32(instr_id),
        c.c_int32(chan),
        acquire_type,
        acquire_meas_V,
        acquire_meas_I,
        acquire_time_stamp,
        load_line_effect_comp,
    )
    check_error(err)


def pulse_meas_rt(instr_id: int, chan: int, v_meas_col_name: str, i_meas_col_name: str,
                  time_stamp_col_name: str, status_col_name: str):
    """configures channel to return pulse source and measure data in pseudo real time.
    As measurements are performed, the data is automatically placed in the Clarius Analyze sheet.
    """
    v_meas_name = make_char_pointer(v_meas_col_name)
    i_meas_name = make_char_pointer(i_meas_col_name)
    timestamp_meas_name = make_char_pointer(time_stamp_col_name)
    status_meas_name = make_char_pointer(status_col_name)

    err = _dll.pulse_meas_rt(c.c_int32(instr_id), c.c_int32(chan), v_meas_name, i_meas_name,
                             timestamp_meas_name, status_meas_name)
    check_error(err)


def pulse_ranges(
    instr_id: int,
    chan: int,
    v_src_range: float,
    v_range_type: int,
    v_range: float,
    i_range_type: int,
    i_range: float,
):
    """set the voltage pulse range and voltage/current measure ranges
    - Range types: Auto 0, Limited auto: 1, Fixed: 2
    - V src ranges: 5 or 20 (into 50 Ω), 10 or 40 (into 1 MΩ)
    - current ranges available depend on the source range and whether the system includes a
     4225-RPM. see manual"""

    v_src_range = c.c_double(v_src_range) if v_src_range else None
    v_range = c.c_double(v_range) if v_range else None
    i_range = c.c_double(i_range) if i_range else None

    err = _dll.pulse_ranges(c.c_int32(instr_id), c.c_int32(chan), v_src_range,
                            c.c_int32(v_range_type), v_range, c.c_int32(i_range_type), i_range)
    check_error(err)


def pulse_remove(instr_id: int, chan: int, voltage: float, state: bool):
    """remove a pulse channel from the test.
    """

    err = _dll.pulse_remove(c.c_int32(instr_id), c.c_int32(chan), c.c_double(voltage),
                            c.c_int32(state))
    check_error(err)


def pulse_sample_rate(instr_id: int, sample_rate: float):
    """ set the measurement sample rate
    """

    err = _dll.pulse_sample_rate(c.c_int32(instr_id), c.c_double(sample_rate))
    check_error(err)


def pulse_source_timing(instr_id: int, chan: int, period: float, delay: float, width: float,
                        rise: float, fall: float):
    """ set the pulse period, width, fall time, rise time and delay time
    """

    period = c.c_double(period) if period else None
    delay = c.c_double(delay) if delay else None
    width = c.c_double(width) if width else None
    rise = c.c_double(rise) if rise else None
    fall = c.c_double(fall) if fall else None

    err = _dll.pulse_source_timing(c.c_int32(instr_id), c.c_int32(chan), period, delay, width, rise,
                                   fall)
    check_error(err)


def pulse_step_linear(instr_id: int, chan: int, step_type: int, start: float, stop: float,
                      step: float):
    """ configure the pulse stepping type
    -Step type:
        PULSE_AMPLITUDE_SP: Sweeps pulse voltage amplitude
        PULSE_BASE_SP: Sweeps base voltage level
        PULSE_DC_SP: Sweeps dc voltage level
        PULSE_PERIOD_SP: Sweeps pulse period
        PULSE_RISE_SP: Sweeps pulse rise time
        PULSE_FALL_SP: Sweeps pulse fall time
        PULSE_WIDTH_SP: Sweeps full-width half-maximum pulse width
        PULSE_DUAL_BASE_SP: Dual sweeps base voltage level
        PULSE_DUAL_AMPLITUDE_SP: Dual sweeps pulse voltage amplitude
        PULSE_DUAL_DC_SP: Dual sweeps dc voltage level
    """

    err = _dll.pulse_step_linear(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(step_type),
                                 c.c_double(start), c.c_double(stop), c.c_double(step))
    check_error(err)


def pulse_sweep_linear(instr_id: int, chan: int, sweep_type: int, start: float, stop: float,
                       step: float):
    """ configure sweeping type
    """
    err = _dll.pulse_sweep_linear(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(sweep_type),
                                  c.c_double(start), c.c_double(stop), c.c_double(step))
    check_error(err)


def pulse_train(instr_id: int, chan: int, v_base: float, v_amplitude: float):
    """
    """
    v_base = c.c_double(v_base) if v_base else None
    v_amplitude = c.c_double(v_amplitude) if v_amplitude else None

    err = _dll.pulse_train(c.c_int32(instr_id), c.c_int32(chan))
    check_error(err)


def rpm_config(instr_id: int, chan: int, modifier: int, value: int):
    """send switching commands to the 4225-RPM. Modifier is KI_RPM_PATHWAY"""

    err = _dll.rpm_config(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(modifier),
                          c.c_int32(value))
    check_error(err)


def seg_arb_sequence(instr_id: int, chan: int, seq_num: int, num_segments, start_v: List[float],
                     stop_v: List[float], time: List[float], trig: List[bool], ssr: List[int],
                     meas_type: List[float], meas_start: List[float], meas_stop: List[float]):
    """ define the parameters for a segment arbitrary waveform pulse-measure sequence
    - sequence_id: unique id to identify sequence
    - see docu
    """
    sequence_id = c.c_int32(seq_num)
    num_segments = c.c_int32(num_segments)
    start_voltages = make_double_array_pointer(len(start_v), start_v)
    stop_voltages = make_double_array_pointer(len(stop_v), stop_v)
    times = make_double_array_pointer(len(time), time)
    trigger_values = make_int_array_pointer(len(trig), trig)
    SSRs = make_int_array_pointer(len(ssr), ssr)
    meas_types = make_double_array_pointer(len(meas_type), meas_type)
    meas_starts = make_double_array_pointer(len(meas_start), meas_start)
    meas_stops = make_double_array_pointer(len(meas_stop), meas_stop)

    err = _dll.seg_arb_sequence(c.c_int32(instr_id), c.c_int32(chan), sequence_id, num_segments,
                                start_voltages, stop_voltages, times, trigger_values, SSRs,
                                meas_types, meas_starts, meas_stops)
    check_error(err)


def seg_arb_waveform(instr_id: int, chan: int, num_seq: int, seq: List[int],
                     seq_loop_count: List[float]):
    """ create a waveform from segments
    """
    sequence_ids = make_int_array_pointer(len(seq), seq)
    seq_loop_counts = make_double_array_pointer(len(seq_loop_count), seq_loop_count)

    err = _dll.seg_arb_waveform(c.c_int32(instr_id), c.c_int32(chan), c.c_int32(num_seq),
                                sequence_ids, seq_loop_counts)
    check_error(err)


def decode_pulse_status(status_bits: int) -> dict:
    """decode the pulse status, see Status-code bit map for pulse_fetch in LPT manual"""

    bit_lengths = {
        "channel": 2,
        "voltage range": 2,
        "current range": 4,
        "V meas overflow": 2,
        "I meas overflow": 2,
        "thresholds": 4,
        "Measurement type": 4,
        "reserved 1": 4,
        "RPM mode": 4,
        "LLEC status": 1,
        "LLEC enabled": 1,
        "sweep skipped": 1,
        "reserved 2": 1
    }
    status = {k: None for k in bit_lengths}
    shift = 0
    for cat, bit_len in bit_lengths.items():
        mask = int("1" * bit_len, 2)  # number of bits to select
        status[cat] = status_bits >> shift & mask
        shift += bit_len

    current_ranges = {
        0: "100 nA (RPM only)",
        1: "1 µA (RPM only)",
        2: "10 µA (RPM only)",
        3: "100 µA",
        4: "1 mA (RPM only)",
        5: "10 mA",
        6: "200 mA",
        7: "800 mA",
    }
    over_flows = {
        0: "No overflow",
        1: "Negative overflow",
        2: "Positive overflow",
    }
    limits = {
        0: "None",
        1: "Source compliance",
        2: "Current threshold reached or surpassed",
        4: "Voltage threshold reached or surpassed",
        8: "Power threshold reached or surpassed",
    }
    meas_types = {0: "?", 1: "Spot", 2: "Waveform", 3: "?"}

    status["current range"] = current_ranges[status["current range"]]
    status["V meas overflow"] = over_flows[status["V meas overflow"]]
    status["I meas overflow"] = over_flows[status["I meas overflow"]]
    status["thresholds"] = limits[status["thresholds"]]
    status["Measurement type"] = meas_types[status["Measurement type"]]

    return status
