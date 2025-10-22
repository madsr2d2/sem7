#
# Simple random cocotb test using random library.
#
import cocotb
import vsc

from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.clock import Clock


@vsc.randobj
class Stim:
    def __init__(self):
        self.data = vsc.rand_uint8_t()

    @vsc.constraint
    def c_lt_10(self):
        self.data < 10  # pyright: ignore


@cocotb.test()
async def sat_random_test(dut):
    """Test sends 10 random inputs."""

    # Create a 2ns period clock on port clk
    clock = Clock(dut.clk, 2, units="ns")  # pyright: ignore

    # Start the clock
    cocotb.start_soon(clock.start())

    # Reset device
    dut.rst.value = 1
    dut.in_data.value = 0
    dut.in_valid.value = 0

    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # Generate 10 random data values
    stim = Stim()  # pyright: ignore
    for _ in range(10):
        await RisingEdge(dut.clk)
        # dut.in_data.value = random.randint(0, 15)
        stim.randomize()
        dut.in_data.value = int(stim.data)
        dut.in_valid.value = 1
