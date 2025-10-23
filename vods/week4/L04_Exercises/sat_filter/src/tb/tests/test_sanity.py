import cocotb
from cocotb.triggers import RisingEdge


@cocotb.test()
async def sanity_drive_all_values(dut):
    # Internal clock in the wrapper is already running
    dut.rst.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst.value = 0

    # Drive 0..15 with valid=1 and observe outputs
    for a in range(16):
        dut.in_valid.value = 1
        dut.in_data.value = a
        await RisingEdge(dut.clk)
        dut._log.info(
            f"a={a:02d} out_valid={int(dut.out_valid.value)} out_data={int(dut.out_data.value)}"
        )
