def parallel_model(A: int, B: int, C: int) -> int:
    """parallel assignment"""

    if A == B:
        out = 1

    if A == C:
        out = 2

    if B == C:
        out = 3
    else:
        out = 0

    return out
