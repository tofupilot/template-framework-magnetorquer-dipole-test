def power_off(measurements, bench, log):
    """Teardown: current off, a last field reading with the rod off so
    the next unit starts from a known cage."""
    bench.set_current(0.0)
    after = bench.field_nt()
    measurements.field_after_nt = after
    log.info(f"Rod off, {after:.1f} nT at the sensor")
