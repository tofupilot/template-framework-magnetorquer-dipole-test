from utils.recipe import INSULATION_V


def electrical(measurements, bench, log):
    """Coil resistance 4-wire and insulation coil-to-case at 500 V DC,
    before any current goes through the rod."""
    r = bench.coil_resistance_ohm()
    ir = bench.insulation_mohm(INSULATION_V)
    measurements.coil_resistance_ohm = r
    measurements.insulation_mohm = ir
    log.info(f"Coil {r:.3f} ohm, insulation {ir:.0f} Mohm at {INSULATION_V:.0f} V")
