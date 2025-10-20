import random

import cocotb
from cocotb.triggers import RisingEdge, ClockCycles, Timer, ReadOnly
from cocotb.clock import Clock

@cocotb.test()
async def mux_basic_test(dut):
  """Test for out=A[1]"""
 
  # Start the clock as the mux RTL is clocked
  # NOTE: NO reset signal in the RTL
  clk = Clock(signal=dut.clk, period=2, units="ns")
  cocotb.start_soon(clk.start())

  # Set A to 11
  # And sel to 1, selecting bit number 1 in A
  # for output
  A   = 11
  sel = 1

  # Drive A and sel
  dut.A.value   = A
  dut.sel.value = sel

  # Await the CLK to let the RTL update state
  await RisingEdge(dut.clk)

  # Wait an extra clock and for the ReadOnly region
  # So RTL has settled
  await RisingEdge(dut.clk)
  await ReadOnly()

  # Check that the MUX is working correctly
  assert dut.out.value == 1, f"Mux result is incorrect"
  
  # Testing different triggers
  await Timer(2, 'ns')
  await ClockCycles(dut.clk, 2)
  await RisingEdge(dut.clk)
  
@cocotb.test()
async def mux_randomized_test(dut):
  """Test for randomizing out=A[sel]"""
 
  # Start the clock as the mux RTL is clocked
  # NOTE: NO reset signal in the RTL
  clk = Clock(signal=dut.clk, period=2, units="ns")
  cocotb.start_soon(clk.start())

  dut.A.value   = 0
  dut.sel.value = 0

  # Sample reset values into DUT
  await RisingEdge(dut.clk)

  # Do 10 random transaction, one per clk.
  for i in range(10):
    # Randomize input stimuli
    A   = random.randint(0, 15)
    sel = random.randint(0,  3)

    # Drive A and sel
    dut.A.value   = A
    dut.sel.value = sel

    # Await the CLK to let the RTL update state
    await RisingEdge(dut.clk)

    # Wait for all delta cycles to settle
    await ReadOnly()

    # Compute expected result
    expected_result = (A >> sel) & 1;

    await RisingEdge(dut.clk)
    
    assert dut.out.value == expected_result, f"Mux result is incorrect"
