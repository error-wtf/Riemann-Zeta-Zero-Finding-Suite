# count_certified.py — counting scaffold (scan fallback)
import mpmath as mp
from zeros_by_scan import find_zeros_scan
def count_by_scan(T1, T2, step=0.02, dps=60, adaptive=False, adapt_scale=0.25):
    """
    Return the number of zeros of Hardy's Z-function in the interval [T1,T2] by scanning.

    For small intervals or illustrative purposes this function uses a simple
    scanning method provided by :func:`find_zeros_scan`.  It can operate
    either with a fixed step size or with an adaptive step tuned to the
    local zero spacing.  Higher `dps` values slow the scan but improve
    accuracy of the zero estimates.

    Args:
        T1: lower bound of the interval.
        T2: upper bound of the interval.
        step: fixed step size when `adaptive` is False.
        dps: decimal precision for mpmath computations.
        adaptive: whether to use adaptive step sizing.
        adapt_scale: scaling factor applied to the local wavelength when
            `adaptive` is True.

    Returns:
        A tuple ``(count, zeros)`` where ``count`` is the number of zeros found
        and ``zeros`` is a list of the approximate ordinates.
    """
    mp.mp.dps = dps
    zeros = find_zeros_scan(T1, T2, coarse_step=step, method="bisect", adaptive=adaptive, adapt_scale=adapt_scale)
    zs = [float(z) for z in zeros]
    return len(zs), zs
# TODO: argument principle with interval arithmetic
