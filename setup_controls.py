import antennas
import utils
import imp


# force module updates
CUSTOM_MODULES = [antennas, utils]
for module in CUSTOM_MODULES:
    imp.reload(module)

CLEAR_LIST = ["Fractionated Dipole Array"]

# array setup parameters
ARRAY_NAME = "Fractionated Dipole Array"
N_DIPOLES = 4
DIPOLE_SETTINGS = {"length": 250,
                   "width": 10,
                   "gapwidth": 2,
                   "thickness": 0,
                   "matchingLEs": False}
FRACTIONATED_DIPOLE_CLASS = antennas.FractionatedDipole
ARRAY_WIDTH = 240
ARRAY_HEIGHT = 300

if __name__ == "__main__":
    # remove old or duplicate entity groups
    utils.clear_from_model(CLEAR_LIST)
    # instantiate array
    frac_dipole_array = antennas.ElipseArray(name=ARRAY_NAME,
                                             n_antennas=N_DIPOLES,
                                             antenna_parameters=DIPOLE_SETTINGS,
                                             antenna_class=FRACTIONATED_DIPOLE_CLASS,
                                             array_width=ARRAY_WIDTH,
                                             array_height=ARRAY_HEIGHT)
