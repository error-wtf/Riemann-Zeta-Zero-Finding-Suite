# zeros_by_scan.py — scan + bisection refinement
import mpmath as mp
from common import Z
def _bisect(a,b,steps=80):
    fa, fb = Z(a), Z(b)
    for _ in range(steps):
        m = (a+b)/2; fm = Z(m)
        if fa*fm <= 0: b, fb = m, fm
        else: a, fa = m, fm
    return (a+b)/2
def _local_wavelength(t):
    """
    Estimate the local oscillation wavelength for Hardy's Z-function.  For
    sufficiently large `t` the spacing between zeros is roughly
    `2*pi/log(t/(2*pi))`.  A floor is applied for `t < 3` to avoid
    division by zero.

    Args:
        t: height on the critical line (mpmath float or Python float).

    Returns:
        A positive float giving the approximate zero spacing.
    """
    t = mp.mpf(t)
    t_ref = max(t, mp.mpf('3.0'))
    return float(2 * mp.pi / mp.log(t_ref / (2 * mp.pi)))


def _adaptive_step(t, scale=0.25, min_step=0.002, max_step=0.08):
    """
    Compute an adaptive step size proportional to the local wavelength.
    The step is clamped into [min_step, max_step] to avoid extreme values.

    Args:
        t: current height (float).
        scale: factor multiplying the local wavelength.
        min_step: lower bound for the step size.
        max_step: upper bound for the step size.

    Returns:
        A float step size.
    """
    dt = scale * _local_wavelength(t)
    return max(min_step, min(max_step, float(dt)))


def find_zeros_scan(
    t_min: float = 10.0,
    t_max: float = 40.0,
    coarse_step: float = 0.02,
    method: str = "bisect",
    adaptive: bool = False,
    adapt_scale: float = 0.25,
    min_step: float = 0.002,
) -> list:
    """
    Scan the interval ``[t_min, t_max]`` for ordinates ``t`` satisfying
    ``Z(t) = 0``.  When a sign change of the Hardy Z-function is detected
    between two consecutive sampling points, a refinement method (currently
    bisection) is applied to approximate the zero.  To prevent missed
    zeros when using adaptive steps, the scanning algorithm implements a
    **repeated halving** strategy: it successively halves the step
    length until either a sign change is found or the halved step falls
    below ``1.5 * min_step``.

    Parameters
    ----------
    t_min, t_max : float
        The lower and upper bounds of the search interval.
    coarse_step : float
        Fixed step size used when ``adaptive`` is ``False``.
    method : str
        Refinement method used to locate zeros once a sign change is detected.
        Only ``"bisect"`` is supported at present.
    adaptive : bool
        If ``True``, the step size is determined by the local wavelength via
        ``_adaptive_step``; otherwise ``coarse_step`` is used.
    adapt_scale : float
        Scaling factor applied to the local wavelength in adaptive mode.
    min_step : float
        Minimum allowed step size in adaptive mode; also controls the
        termination of the halving procedure (see above).

    Returns
    -------
    list of float
        Approximate ordinates of zeros detected in the interval.
    """
    zeros = []
    t = mp.mpf(t_min)
    f = Z(t)
    # Continue until we reach t_max
    while t < t_max:
        # Determine the nominal step
        dt = (
            _adaptive_step(t, scale=adapt_scale, min_step=min_step, max_step=0.08)
            if adaptive
            else float(coarse_step)
        )
        dt_cur = dt
        sign_found = False
        # Probe with repeated halving until sign change detected or step too small
        while True:
            t_candidate = mp.mpf(min(t_max, t + dt_cur))
            g = Z(t_candidate)
            # If current value is exactly zero, record and break (rare)
            if f == 0:
                zeros.append(float(t))
                sign_found = True
                t, f = t_candidate, g
                break
            # If sign change detected, refine and update
            if f * g < 0:
                # Determine the bracket and apply refinement
                a, b = t, t_candidate
                if method == "bisect":
                    zeros.append(float(_bisect(a, b)))
                else:
                    zeros.append(float(_bisect(a, b)))
                # Update state to the candidate point
                t, f = t_candidate, g
                sign_found = True
                break
            # Otherwise, if adaptive, halve dt_cur until threshold reached
            if adaptive and dt_cur > min_step * 1.5:
                dt_cur *= 0.5
                continue
            break
        # If no sign change, advance by full step
        if not sign_found:
            t_next = mp.mpf(min(t_max, t + dt))
            # Avoid infinite loop if dt == 0
            if t_next == t:
                break
            f = Z(t_next)
            t = t_next
    return zeros
