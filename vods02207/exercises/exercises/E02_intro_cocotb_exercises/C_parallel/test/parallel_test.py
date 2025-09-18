import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge, Combine, Join, First
from ref_model.parallel_model import parallel_model


async def drive_signal_after_random_interval(name: str, value: int, dut):
    wait_clks = random.randint(1, 5)
    await ClockCycles(dut.clk, wait_clks)
    signal = getattr(dut, name)
    signal.value = value & ((1 << len(signal)) - 1)


@cocotb.test()  # pyright: ignore
async def drive_signals(dut):
    # start clock
    clk = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clk.start())

    for _ in range(20):
        # Generate random driven values ltst
        values = [random.randint(0, 15) for _ in range(3)]

        # Sechdule tasks to drive signals after random intervals
        task_a = cocotb.start_soon(
            drive_signal_after_random_interval("A", values[0], dut)
        )
        task_b = cocotb.start_soon(
            drive_signal_after_random_interval("B", values[1], dut)
        )
        task_c = cocotb.start_soon(
            drive_signal_after_random_interval("C", values[2], dut)
        )

        # Wait for all tasks to complete
        await Combine(Join(task_a), Join(task_b), Join(task_c))
        await First(Join(task_a), Join(task_b), Join(task_c))

        await RisingEdge(dut.clk)
        await ReadOnly()

        # Verify output
        expected = parallel_model(values[0], values[1], values[2])
        got = int(dut.out.value)

        assert got == expected, (
            f"A:{values[0]}, B:{values[1]}, C:{values[2]} => got: {got}, expected: {expected}"
        )
