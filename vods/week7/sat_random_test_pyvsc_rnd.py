#
# Simple random cocotb test using PyVSC library.
#

import cocotb
import vsc

from cocotb.triggers import RisingEdge, ClockCycles, ReadOnly
from cocotb.clock import Clock
from cocotb.binary import BinaryValue

from utilities import create_coverage_report
from sat_filter_coverage import covergroup_ssdt

import warnings
# Quick fix because of warnings of PyVSC
warnings.simplefilter("ignore")

@vsc.randobj
class sat_data_obj(object):

    def __init__(self):
        self.in_data = vsc.rand_bit_t(4)

    @vsc.constraint
    def valid_data(self):
        self.in_data >= 0
        self.in_data <= 10


@cocotb.test()
async def sat_random_test(dut):
    """ Test sends 10 random inputs.
    """

    # Create a 2ns period clock on port clk
    clock = Clock(dut.clk, 2, units="ns")

    # Start the clock
    cocotb.start_soon(clock.start())

    # Create coverage
    # ------ 2 implementations possible -------------

    # ------ (1)
    #coverage = covergroup_ssdt("ssdt_coverage", )

    # ------ (2)
    # Start "coverage_sampling" coroutine concurrently
    coverage_task = cocotb.start(coverage_sampling(dut))
    await coverage_task

    # -------------------------------------------------

    # Resetting input values
    dut.in_data.value = 0
    dut.in_valid.value = 0

    # Reset device
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    await RisingEdge(dut.clk)
    dut.in_valid.value = 1

    # Randomized object
    rand_obj = sat_data_obj()

    # Randomize and send data
    for _ in range(10):

        # Randomize object
        rand_obj.randomize()

        # Setting values to DUT
        dut.in_data.value = BinaryValue(rand_obj.in_data).integer

        # Wait set value
        await ClockCycles(dut.clk, 1)

        # ------ (1)
        # Coverage sampling
        #if dut.out_valid.value == 1:
            #coverage.sample(dut.out_data.value)

    # Reset input values
    dut.in_data.value = 0
    dut.in_valid.value = 0

    await ClockCycles(dut.clk, 2)

    # ------ (2)
    coverage_task.close()

    create_coverage_report("sat_random_test_pyvsc")

# ------ (2)
# Coroutine to check 'out_valid' before
async def coverage_sampling(dut):
    """ Waits for 'out_valid' high to sample.
    """

    coverage = covergroup_ssdt("ssdt_coverage", )

    while True:

        await ReadOnly()
        await RisingEdge(dut.clk)

        while dut.out_valid.value != 1:
            await RisingEdge(dut.clk)

        coverage.sample(dut.out_data.value)
