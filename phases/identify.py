def identify(measurements, bench, unit, log):
    """Setup: rod marking, sensor distance on the record, cage nulled
    with the rod unpowered. The dipole numbers are only as good as the
    field the cage leaves at the sensor."""
    ident = bench.identify()
    measurements.rod_marking = ident["rod_marking"]
    measurements.cage_residual_nt = bench.cage_null()
    unit.metadata["sensor_distance_m"] = ident["sensor_distance_m"]
    log.info(f"Rod {unit.serial_number} marked {ident['rod_marking']}, sensor at {ident['sensor_distance_m']:.2f} m, cage residual {measurements.cage_residual_nt} nT")
