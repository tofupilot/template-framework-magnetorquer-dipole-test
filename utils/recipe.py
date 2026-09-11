"""Magnetorquer acceptance recipe for a 1 A·m²-class torque rod
(a coil on a high-permeability core, 5 V, 150 mA rated).

The dipole moment is measured on the axis of the rod with a fluxgate
magnetometer at a known distance inside a Helmholtz cage that nulls
the Earth's field: on axis, B = (mu0 / 2 pi) m / r³, so 1 A·m² at
0.5 m reads 1600 nT. The vendor sheets this class of rod is modelled
on (NewSpace Systems, ZARM, CubeSpace) quote the dipole at rated
current with a linearity figure, the residual dipole with the current
off (the core's remanence, the number the attitude control model has
to live with), the coil resistance and the insulation to the case.
None of the numbers below are a standard's; they are the rod's data
sheet, and the cage residual is the facility's own."""

RATED_CURRENT_A = 0.150
RATED_DIPOLE_AM2 = 1.0
COIL_V = 5.0
COIL_R_OHM = 33.0
COIL_R_TOL_PCT = 5.0
INSULATION_V = 500.0
INSULATION_MOHM_MIN = 100.0

SWEEP_CURRENT_A = [round(-0.150 + 0.025 * i, 3) for i in range(13)]  # -150 .. +150 mA
DIPOLE_AT_RATED_MIN_AM2 = 0.95
LINEARITY_PCT_MAX = 2.0          # worst deviation from the straight fit, % of rated
RESIDUAL_AM2_MAX = 0.010         # remanent dipole with the current off, after +rated
GAIN_AM2_PER_A_MIN = 6.3         # slope of the fit
POLARITY_AXIS = "+X"             # positive current must give a moment along the rod's +X mark

SENSOR_DISTANCE_M = 0.50
CAGE_RESIDUAL_NT_MAX = 50.0      # field at the sensor with the cage nulling and the rod off
MU0_OVER_2PI = 2.0e-7            # T·m/A
