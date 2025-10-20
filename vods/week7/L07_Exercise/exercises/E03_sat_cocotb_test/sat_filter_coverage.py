import vsc


width = 4


@vsc.covergroup
class covergroup_ssdt(object):
    def __init__(self):
        self.vsc.with_sample(data=vsc.bit_t(width))
        self.cp1 = vsc.coverpoint(
            self.data,
            bins={"a": vsc.bin(0), "b": (1 << width) - 1, "c": [0, (1 << width) - 1]},
        )
