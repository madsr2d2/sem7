from pyuvm import uvm_object

from uvc.ssdt.src.uvc_ssdt_config import uvc_ssdt_config
from vods.week9.L09_Exercise.summer.src.tb.uvc.ssdt.src.uvc_ssdt_interface import (
    ssdt_interface_wrapper,
)

from uvc.ssdt.src.ssdt_common import uvc_ssdt_type_enum, SequenceItemOverride,
from uvc.ssdt.src.uvc_ssdt_agent import uvc_ssdt_agent
from pyuvm import uvm_env, uvm_active_passive_enum, ConfigDB

class summer_tb_config(uvm_object):
    def __init__(self, name="cl_sdt_tb_config"):
        super().__init__(name)

        # self.data_width = None
        # self.threshold = None
        #
        self.dut = None
        self.ssdt_prod_cfg = uvc_ssdt_config.create("ssdt_prod_cfg")
        self.ssdt_cons_cfg = uvc_ssdt_config.create("ssdt_cons_cfg")

        self.ssdt_prod_cfg.vif = ssdt_interface_wrapper(name="producer_interface")
        self.ssdt_cons_cfg.vif = ssdt_interface_wrapper(name="consumer_interface")

        ConfigDB().set(self,"uvc_ssdt_consumer", "cfg", self.cfg.ssdt_cons_cfg)
        self.ssdt_cons_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.ssdt_cons_cfg.driver_type = uvc_ssdt_type_enum.CONSUMER
        self.ssdt_cons_cfg.seq_item_override = SequenceItemOverride.USER_DEFINED

        ConfigDB().set(self,"uvc_ssdt_producer", "cfg", self.cfg.ssdt_prod_cfg)
        self.ssdt_prod_cfg.is_active         = uvm_active_passive_enum.UVM_ACTIVE
        self.ssdt_prod_cfg.driver_type       = uvc_ssdt_type_enum.PRODUCER
        self.ssdt_prod_cfg.seq_item_override = SequenceItemOverride.USER_DEFINED

    def build_phase(self):
        self.ssdt_prod_cfg.DATA_WIDTH = self.data_width
        self.ssdt_cons_cfg.DATA_WIDTH = self.data_width
