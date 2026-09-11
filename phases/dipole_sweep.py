import numpy as np

from utils.recipe import (CAGE_RESIDUAL_NT_MAX, MU0_OVER_2PI, POLARITY_AXIS, RATED_CURRENT_A,
                          RATED_DIPOLE_AM2, SENSOR_DISTANCE_M, SWEEP_CURRENT_A)


def dipole_sweep(measurements, bench, log):
    """Current stepped from -rated to +rated, the axial field read at
    each step and converted to a dipole through the on-axis law. The
    zero-current field is subtracted as the cage residual. Judged on the
    dipole at rated current, the straightness of the curve, the gain and
    the polarity against the rod's marking."""
    bench.set_current(0.0)
    b0 = bench.field_nt()
    field = []
    for amps in SWEEP_CURRENT_A:
        bench.set_current(amps)
        field.append(bench.field_nt())
    bench.set_current(0.0)
    b = np.array(field) - b0
    m = b * 1e-9 * SENSOR_DISTANCE_M ** 3 / MU0_OVER_2PI  # A·m²
    i = np.array(SWEEP_CURRENT_A)
    gain, offset = np.polyfit(i, m, 1)
    resid_pct = 100.0 * np.abs(m - (gain * i + offset)).max() / RATED_DIPOLE_AM2
    at_rated = float(m[np.argmin(np.abs(i - RATED_CURRENT_A))])
    polarity = "+X" if at_rated > 0 else "-X"

    measurements.sweep.x_axis = SWEEP_CURRENT_A
    measurements.sweep.y_axis.dipole = m.round(4).tolist()
    measurements.sweep.y_axis.dipole.aggregations.at_rated_am2 = at_rated
    measurements.sweep.y_axis.dipole.aggregations.gain_am2_per_a = float(gain)
    measurements.sweep.y_axis.dipole.aggregations.linearity_pct = float(resid_pct)
    measurements.polarity = polarity
    log.info(f"Dipole {at_rated:.3f} A·m² at {RATED_CURRENT_A * 1000:.0f} mA, gain {gain:.2f} A·m²/A, worst deviation from straight {resid_pct:.2f} % of rated, polarity {polarity} (marking {POLARITY_AXIS})")
