"""SSDT-UVC Coverage collector"""

import vsc
from pyuvm import uvm_subscriber, ConfigDB
from .uvc_ssdt_seq_item import uvc_ssdt_seq_item


class uvc_ssdt_coverage(uvm_subscriber):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.cfg = None

    def build_phase(self):
        self.logger.debug("build_phase() SSDT_Coverage")
        super().build_phase()

        # Create the covergroup
        # Get the configuration object
        self.cfg = ConfigDB().get(self, "", "cfg")

        self.cg_ssdt = covergroup_ssdt(
            f"{self.get_full_name()}.cg_ssdt", self.cfg.DATA_WIDTH
        )

    # "write" method to sample the covergroups
    def write(self, item: uvc_ssdt_seq_item):
        self.cg_ssdt.sample(item.data)


@vsc.covergroup
class covergroup_ssdt(object):
    def __init__(self, name, ssdt_width):
        self.options.name = name

        self.with_sample(data=vsc.bit_t(ssdt_width))

        MAX = 2**ssdt_width

        self.cp_data = vsc.coverpoint(
            self.data,
            bins={
                "0": vsc.bin(0),
                "max": vsc.bin(MAX - 1),
                "range": vsc.bin_array([4], [1, MAX - 2]),
            },
        )
