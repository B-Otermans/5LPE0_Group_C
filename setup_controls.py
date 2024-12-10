import antennas
import utils


CUSTOM_MODULES = [antennas, utils]
CLEAR_LIST = ["Fractionated Dipole Array"]

# array setup parameters
N_DIPOLES = 12
DIPOLE_SETTINGS = {"length": 250,
                   "width": 10,
                   "gapwidth": 2,
                   "thickness": 0,
                   "matchingLEs": False}
FRACTIONATED_DIPOLE_CLASS = antennas.FractionatedDipole
ARRAY_WIDTH = 240
ARRAY_HEIGHT = 300

if __name__ == "__main__":
    # force module updates
    utils.update_modules(CUSTOM_MODULES)
    # remove old or duplicate entity groups
    utils.clear_from_model(CLEAR_LIST)
    # instantiate array
    frac_dipole_array = antennas.elipse_array(n_antennas=N_DIPOLES,
                                              antenna_parameters=DIPOLE_SETTINGS,
                                              antenna_class=FRACTIONATED_DIPOLE_CLASS,
                                              array_width=ARRAY_WIDTH,
                                              array_height=ARRAY_HEIGHT)
    frac_dipole_array.Name = "Fractionated Dipole Array"
