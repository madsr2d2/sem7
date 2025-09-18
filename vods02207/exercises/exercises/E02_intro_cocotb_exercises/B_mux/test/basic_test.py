
# Simple tests for an adder module
import random
import cocotb
from cocotb.triggers import ReadOnly, RisingEdge, Timer, ClockCycles
from ref_model.mux_model import mux_model
from cocotb.clock import Clock


@cocotb.test() # pyright: ignore
async def mux_basic_test(dut):
    """Static test of mux moduel"""

    clk = Clock(dut.clk, 10, units = 'ns')
    cocotb.start_soon(clk.start())

    A = 15
    sel = 0

    await ClockCycles(dut.clk, 5)

    dut.A.value = A
    dut.sel.value = sel

    # await Timer(2, units="ns")
    await RisingEdge(dut.clk)
    await ReadOnly()

    expected = mux_model(A,sel)
    got = int(dut.out.value)

    assert got == expected, f"Result incorrect: A={A:04b}, sel={sel:02b}, got={got}, expected={expected}"


@cocotb.test() # pyright: ignore
async def mux_randomised_test(dut):
    """Random mux test"""

    clk = Clock(dut.clk, 10, units = 'ns')
    cocotb.start_soon(clk.start())


    for _ in range(10):
        await ClockCycles(dut.clk, 2)

        A = random.randint(0, 15)
        sel = random.randint(0, 3)

        dut.A.value = A
        dut.sel.value = sel

        await RisingEdge(dut.clk)
        await ReadOnly()

        expected = mux_model(A,sel)
        got = int(dut.out.value)

        assert got == expected, f"Result is incorrect: A={A:04b}, sel={sel:02b}, got={got}, expected={expected}"

