from utils.recipe import MU0_OVER_2PI, RATED_CURRENT_A, SENSOR_DISTANCE_M


def residual(measurements, bench, log):
    """Remanent dipole: the rod driven to +rated, the current cut, the
    field read with the cage still nulling. What the core keeps is a
    permanent disturbance torque the attitude model has to carry. The
    zero reference is the cage residual read again here, not the setup
    value: phases cannot read each other's measurements back."""
    bench.set_current(RATED_CURRENT_A)
    bench.set_current(0.0)
    b = bench.field_nt() - bench.cage_null()
    m = b * 1e-9 * SENSOR_DISTANCE_M ** 3 / MU0_OVER_2PI
    measurements.residual_am2 = float(abs(m))
    log.info(f"Residual dipole {abs(m) * 1000:.1f} mA·m² after +{RATED_CURRENT_A * 1000:.0f} mA")
