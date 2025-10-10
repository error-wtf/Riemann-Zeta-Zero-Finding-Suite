import mpmath as mp
from rigorous_Z import eval_ZZp_interval, sign_from_interval
from certify_zero import certify_zero_unique

def _local_wavelength(t: float) -> float:
    """
    Estimate the local oscillation wavelength of Hardy's Z-function.

    For large t the oscillations have a characteristic spacing of roughly
    :math:`2\pi / \log(t/(2\pi))`. We cap the argument below to avoid
    division by zero for very small t.

    Args:
        t: height on the critical line (real).

    Returns:
        A positive float giving the approximate spacing between successive
        zeros near t.
    """
    t_ref = max(mp.mpf(t), mp.mpf('3.0'))
    return float(2 * mp.pi / mp.log(t_ref / (2 * mp.pi)))


def _adaptive_step(t: float, scale: float, min_step: float, max_step: float) -> float:
    """
    Compute an adaptive step size based off the local wavelength.  The
    step size is proportional to the estimated wavelength but clamped to
    lie within ``[min_step, max_step]`` to avoid unreasonably small or
    large jumps.

    Args:
        t: current height on the critical line.
        scale: scaling factor applied to the local wavelength estimate.
        min_step: minimum allowed step size.
        max_step: maximum allowed step size.

    Returns:
        A positive float representing the step length to use when
        advancing from t.
    """
    dt = scale * _local_wavelength(t)
    return float(max(min_step, min(max_step, dt)))


def run_block(T1, T2, scan_step=0.02, eps=1e-10, dps=80, rad=1e-12,
              adaptive=False, adapt_scale=0.25, min_step=0.002, max_step=0.05):
    """
    Enumerate and certify zeros of Hardy's Z-function in a block [T1, T2].

    This routine performs a simple scanning pass to detect sign changes in
    Z(t) and then calls a rigorous certification routine on each bracket
    where a sign change occurs.  By default a fixed ``scan_step`` is used
    between successive samples, mirroring the behaviour of earlier
    versions of this script.  If ``adaptive`` is set to True then the
    spacing between samples is chosen dynamically based on the local
    wavelength estimate ``2π/log(t/(2π))``.  The adaptive step is
    clamped within ``[min_step, max_step]`` and scaled by
    ``adapt_scale``.  These defaults yield a reasonably fine mesh while
    avoiding unnecessary oversampling at large heights.

    Args:
        T1: lower end of the height interval (real).
        T2: upper end of the height interval (real).
        scan_step: fixed step size for scanning when ``adaptive`` is False.
        eps: target width for certified zero brackets.
        dps: decimal precision for mpmath computations.
        rad: radius used for interval evaluations in ``eval_ZZp_interval``.
        adaptive: if True, use adaptive step sizing based off the local
            wavelength; otherwise use the fixed ``scan_step``.
        adapt_scale: scale factor for the adaptive step (ignored if
            ``adaptive`` is False).
        min_step: minimum allowed adaptive step (ignored if ``adaptive`` is False).
        max_step: maximum allowed adaptive step (ignored if ``adaptive`` is False).

    Returns:
        A dictionary with metadata for the block, including a list of
        zero certificates.  The keys include ``"T1"``, ``"T2"``,
        ``"dps"``, ``"eps"`` and ``"certificates"``.
    """
    T1 = float(T1)
    T2 = float(T2)
    mp.mp.dps = max(dps, 60)
    t = T1
    Z_iv, _, _ = eval_ZZp_interval(t, rad=rad, dps=dps)
    s_prev = sign_from_interval(Z_iv)
    t_prev = t
    certs = []
    while t < T2:
        # Determine base step (adaptive or fixed)
        dt = _adaptive_step(t, adapt_scale, min_step, max_step) if adaptive else float(scan_step)
        dt_cur = dt
        # Retrieve current sign and maintain a flag to indicate if we found a sign change
        sign_found = False
        # Repeatedly halve the step until a sign change is found or the step becomes too small
        while True:
            t_candidate = min(T2, t + dt_cur)
            ZN, _, _ = eval_ZZp_interval(t_candidate, rad=rad, dps=dps)
            s_next = sign_from_interval(ZN)
            # Only act if we have definite sign information on both ends
            if s_prev in ("pos", "neg") and s_next in ("pos", "neg") and s_prev != s_next:
                # Sign change detected in [t_prev, t_candidate]
                ok, interval, cert = certify_zero_unique(t_prev, t_candidate, eps=eps, dps=dps, rad0=rad)
                certs.append(cert)
                # Move to the candidate point and update state
                t_prev, s_prev = t_candidate, s_next
                t = t_candidate
                sign_found = True
                break
            # If no sign change and adaptive scanning is enabled, attempt to halve further
            # Break if fixed scanning or the step is already small
            if (not adaptive) or (dt_cur <= min_step * 1.5):
                break
            # Halve the step and try again
            dt_cur *= 0.5
        # If no sign change found, advance by the full step (or to T2) and update state
        if not sign_found:
            t_next = min(T2, t + dt)
            if t_next == t:  # avoid infinite loop if dt_cur rounds to zero
                break
            # Evaluate sign at the end of the full step
            ZN, _, _ = eval_ZZp_interval(t_next, rad=rad, dps=dps)
            s_next = sign_from_interval(ZN)
            t_prev, s_prev = t_next, s_next
            t = t_next
    return {
        "T1": T1,
        "T2": T2,
        "dps": dps,
        "eps": eps,
        "adaptive": adaptive,
        "adapt_scale": adapt_scale if adaptive else None,
        "certificates": certs
    }
