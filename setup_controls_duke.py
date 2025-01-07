import antennas
import utils
import imp


# force module update
CUSTOM_MODULES = [antennas, utils]
for module in CUSTOM_MODULES:
    imp.reload(module)

CLEAR_LIST = ["Fractionated Dipole Array", "Spacer Group", "Bounding Box"]

# array setup parameters
ARRAY_NAME = "Fractionated Dipole Array"
N_DIPOLES = 8
DIPOLE_SETTINGS = {"length": 350,
                   "width": 10,
                   "gapwidth": 2,
                   "thickness": 0,
                   "matchingLEs": False}
FRACTIONATED_DIPOLE_CLASS = antennas.FractionatedDipole
ARRAY_WIDTH = 170  # in millimeters
ARRAY_HEIGHT = 260  # in millimeters
SPACER_THICKNESS = 10  # in millimeters

# phantom setup parameters
PHANTOM_NAME = "Duke"
PHANTOM_SCALE_FACTOR = 0.95  # e.g. 1.05 for 5% increase, or 0.95 for 5% decrease

# if-statement to only perform model setup when this file is run directly
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
    frac_dipole_array.add_spacers(SPACER_THICKNESS)
    frac_dipole_array.add_bounding_box()
    # align phantom
    utils.align_duke()
    # scale phantom
    utils.scale_model(model_name=PHANTOM_NAME, scale_factor=PHANTOM_SCALE_FACTOR)
