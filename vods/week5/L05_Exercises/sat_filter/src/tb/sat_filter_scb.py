"""Saturation Filter Scoreboard
- Verification component that contains checkers and verifies the functionality of the design.
- Receives transaction level objects captured from the interfaces of a DUT via TLM Analysis Ports.
- Includes the Reference Model.
"""

import cocotb
from pyuvm import uvm_scoreboard, uvm_analysis_port, uvm_tlm_analysis_fifo, ConfigDB
from cocotb.queue import Queue


class sat_filter_scoreboard(uvm_scoreboard):
    """Scoreboard for Saturation Filter."""

    def __init__(self, name="sat_filter_scoreboard", parent=None):
        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None

        self.analysis_port = None  # Analysis Port handler

        # FIFO for connecting to UVC's ap
        self.uvc_ssdt_consumer_fifo = None
        self.ref_model_fifo = None

        # recording number of successes and failures
        self.succes = 0
        self.failure = 0

    def build_phase(self):
        super().build_phase()

        # Get the configuration object
        self.cfg = ConfigDB().get(self, "", "cfg")
        self.logger.debug(
            f" Config of < {self.get_name()} > is {(self.cfg.__getattribute__)}"
        )

        # Instantiate the analysis port
        self.analysis_port = uvm_analysis_port(f"{self.get_name()}_analysis_port", self)

        # Create the analysis FIFOs
        self.uvc_ssdt_consumer_fifo = uvm_tlm_analysis_fifo(
            "uvc_ssdt_consumer_fifo", self
        )
        self.ref_model_fifo = uvm_tlm_analysis_fifo("ref_model_fifo", self)

        # Queues to store output of Ref. Model
        self.uvc_ssdt_consumer_queue = Queue(maxsize=1)
        self.ref_model_queue = Queue(maxsize=1)

    async def run_phase(self):
        """
        - Get the item from the FIFOs
        - Compare the samples received
        """

        await super().run_phase()
        # Start the sampling coroutines
        cocotb.start_soon(
            self.sample_ap_uvc(
                self.uvc_ssdt_consumer_fifo,
                self.uvc_ssdt_consumer_queue,
            )
        )
        cocotb.start_soon(
            self.sample_ap_uvc(
                self.ref_model_fifo,
                self.ref_model_queue,
            )
        )

        while True:
            # Get the items
            self.uvs_ssdt_consumer_item = await self.uvc_ssdt_consumer_queue.get()
            self.ref_model_item = await self.ref_model_queue.get()

    # Report the results of the comparisons
    def check_phase(self):
        super().check_phase()

    async def sample_ap_uvc(self, fifo, queue):
        """copy fifo items into queue"""
        while True:
            item = await fifo.get()
            item.set_dame(fifo.get_name())

            await queue.put(item)
            self.logger.debug(f"sample_ap_uvc: {item} |")
