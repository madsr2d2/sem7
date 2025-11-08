from pyuvm import *
import vsc


class sat_filter_coverage(uvm_subscriber):
    def __init__(self, name):
        super().__init__(name)
        self.cfg = None
        self.cg_ssdt = None

    def build_phase(self):
        # Get the configuration object
        self.cfg = ConfigDB().get(self, "", "cfg")


@vsc.covergroup
class covergroup_ssdt(object):
    def __init__(self, name, ssdt_width):
        self.options.name = name
        self.options.ssdt_width = ssdt_width
