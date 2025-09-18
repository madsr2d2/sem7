
def mux_model(A: int, sel: int) -> int:
    """model of mux"""
    return ( A >> sel ) & 1

