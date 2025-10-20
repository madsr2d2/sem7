#__RELEASE_REMOVE_TOTAL__
import random

import cocotb
from cocotb.triggers import RisingEdge, ClockCycles, Combine, First, Timer
from cocotb.types import LogicArray
from cocotb.clock import Clock

@cocotb.test()
async def parallel_test_combine(dut):

    cocotb.start_soon(Clock(signal=dut.clk,period=2,units='ns').start())

    coroutineA = cocotb.start_soon(drive_signal_A(dut))
    coroutineB = cocotb.start_soon(drive_signal_B(dut))
    coroutineC = cocotb.start_soon(drive_signal_C(dut))

    await Combine(coroutineA, coroutineB, coroutineC)

@cocotb.test()
async def wait(dut):
    dut.clk.value = LogicArray('x')
    dut.A.value = LogicArray('x'*4)
    dut.B.value = LogicArray('x'*4)
    dut.C.value = LogicArray('x'*4)

    await Timer(10, 'ns')

@cocotb.test()
async def parallel_test_first(dut):

    cocotb.start_soon(Clock(signal=dut.clk,period=4,units='ns').start())

    coroutineA = cocotb.start_soon(drive_signal_A(dut))
    coroutineB = cocotb.start_soon(drive_signal_B(dut))
    coroutineC = cocotb.start_soon(drive_signal_C(dut))

    first_done = await First(coroutineA, coroutineB, coroutineC)
    print(first_done)

async def drive_signal_A(dut):
    await RisingEdge(dut.clk)

    for _ in range(20):
        A = random.randint(0, 7)
        dut.A.value = A
        await ClockCycles(dut.clk, 3)

    dut.A.value = LogicArray('x'*4)

async def drive_signal_B(dut):
    await RisingEdge(dut.clk)

    for _ in range(15):
        B = random.randint(0, 7)
        dut.B.value = B
        await ClockCycles(dut.clk, 5)

    dut.B.value = LogicArray('x'*4)

async def drive_signal_C(dut):
    await RisingEdge(dut.clk)

    for _ in range(10):
        C = random.randint(0, 7)
        dut.C.value = C
        await ClockCycles(dut.clk, 8)

    dut.C.value = LogicArray('x'*4)