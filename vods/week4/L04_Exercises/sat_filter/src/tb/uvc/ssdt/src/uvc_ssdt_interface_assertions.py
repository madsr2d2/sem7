""" SSDT interface asserations wrapper"""

import pyuvm
from pyuvm import *
from cocotb.triggers import RisingEdge

class ssdt_interface_assert_check():

    def __init__(self, clk_signal = None, rst_signal = None, valid_signal = None, data_signal = None, name = "ssdt_interface_assert_check"):

        self.name  = name

        self.clk   = clk_signal
        self.rst   = rst_signal

        self.valid = valid_signal
        self.data  = data_signal

        # Set as false if any assertion fail
        self.passed = True

        # The data width interface
        self.DATA_WIDTH = None

    def _set_width_values(self, DATA_WIDTH = 1):
        self.DATA_WIDTH = DATA_WIDTH


    async def check_assertions(self):
        cocotb.start_soon(self.reset_values())

    # Reset requirement (PR 1): 
    # If RST = 1, then VALID cannot be 1
    async def reset_values(self):
        while True:
            try:
                if self.rst.value.binstr == '1':
                    assert self.valid.value.binstr != '1', \
                        f"When reset, valid was {self.valid.value.binstr}"
            except AssertionError as msg:
                self.passed = False
                print(msg)

            # Wait 1 clk cycle
            await RisingEdge(self.clk)


    
    # Data valitidy requirement (PR 2):


  
    # Data invalidity requirement (PR 3):
