import os

import cocotb

from cocotb.triggers import Timer, RisingEdge, ClockCycles
from cocotb.clock import Clock


@cocotb.test()
async def mux_basic_test(dut):
    """Test for out=A[1]"""
    shift = 3
    sel = shift
    A = 1 << shift

    # Start the clock as the mux RTL is clocked
    # NOTE: NO reset signal in the RTL

    clk = Clock(signal=dut.clk, period=2, units="ns")
    cocotb.start_soon(clk.start())
    dut.A.value = A
    dut.sel.value = sel
    cocotb.log.info(dir(dut))

    await ClockCycles(dut.clk, 5)

    expected = (A >> sel) & 1
    assert dut.out.value == expected, "Multiplexer result is incorrect"


@cocotb.test()
async def mux_randomized_test(dut):
    """Test for randomizing out=A[sel]"""

    # Start the clock as the mux RTL is clocked
    # NOTE: NO reset signal in the RTL
    clk = Clock(signal=dut.clk, period=2, units="ns")
    cocotb.start_soon(clk.start())
