import vsc

@vsc.covergroup
class covergroup_ssdt(object):
    
    def __init__(self, name):

        self.options.name = name

        # Define the parameters accepted by the sample function
        self.with_sample(
            data = vsc.bit_t(4),
        )

        MAX_VALUE = (2**4)

        self.cp_data = vsc.coverpoint(self.data, bins={
            "data_0" :          vsc.bin(0),
            "data_max" :        vsc.bin(MAX_VALUE-1),
            "data_others" :     vsc.bin([1, MAX_VALUE-2])
            }
        )
