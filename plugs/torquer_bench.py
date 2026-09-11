"""Magnetorquer bench (mock): a three-axis Helmholtz cage with its
nulling supplies, a fluxgate magnetometer on the rod's axis, a
precision current source on the coil, a micro-ohm meter and an
insulation tester through a switch box.

Maps to a Bartington Mag-03 or Mag-13 fluxgate on a Spectramag or
NI DAQ, a cage of the Ferronato or in-house class driven by three
bipolar supplies, a Keithley 2450 as the coil source, a Hioki RM3545
for the 4-wire resistance and a Megger MIT for the 500 V insulation.
The mock synthesizes a healthy rod: 1.02 A·m² at 150 mA with the
core's gentle saturation at the ends of the sweep, 0.6 % remanence
after the positive rated pulse, 33.2 ohm, insulation over 1 Gohm, and
a cage that nulls to 12 nT. Swap for classes speaking SCPI and the
DAQ's API; the phases stay unchanged.
"""

import numpy as np

from utils.recipe import MU0_OVER_2PI, RATED_CURRENT_A, SENSOR_DISTANCE_M


class TorquerBench:
    def __init__(self):
        self._rng = np.random.default_rng(1007)
        self._gain = 7.0 + self._rng.normal(0.0, 0.05)   # A·m² per A, small-signal
        self._sat_a = 0.60                                # soft saturation knee of the core
        self._remanence = 0.0                             # A·m² left in the core
        self._coil_r = 33.2 + self._rng.normal(0.0, 0.1)
        self._cage_residual_nt = 12.0
        self._current = 0.0
        # self.mag = ...; self.src = pyvisa...; self.cage = ...; self.rm = ...; self.ir = ...
        print("Torquer bench ready, cage nulling, rod unpowered")

    def identify(self):
        return {"rod_marking": "MTQ-1-X", "sensor_distance_m": SENSOR_DISTANCE_M}

    def cage_null(self):
        """Cage supplies trimmed; the field left at the sensor, nT."""
        return round(self._cage_residual_nt + abs(self._rng.normal(0.0, 2.0)), 1)

    def coil_resistance_ohm(self):
        return round(self._coil_r + self._rng.normal(0.0, 0.02), 3)

    def insulation_mohm(self, volts):
        return round(2400.0 + self._rng.normal(0.0, 150.0), 0)

    def set_current(self, amps):
        self._current = float(amps)
        # The core remembers the last large excursion.
        self._remanence = 0.006 * np.sign(amps) if abs(amps) >= RATED_CURRENT_A - 1e-6 else self._remanence

    def _dipole(self, amps):
        return self._gain * self._sat_a * np.tanh(amps / self._sat_a) + self._remanence

    def field_nt(self):
        """Axial field at the sensor from the rod, nT, cage residual and
        sensor noise included."""
        m = self._dipole(self._current)
        b = MU0_OVER_2PI * m / SENSOR_DISTANCE_M ** 3 * 1e9
        return round(b + self._cage_residual_nt + self._rng.normal(0.0, 1.5), 1)

    def __del__(self):
        print("Rod off, cage off")
