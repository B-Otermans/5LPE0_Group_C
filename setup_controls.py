import antennas
import utils
import imp

# force module update
CUSTOM_MODULES = [antennas, utils]
for module in CUSTOM_MODULES:
    imp.reload(module)

CLEAR_LIST = ["Fractionated Dipole Array", "Spacer Group"]

# array setup parameters
ARRAY_NAME = "Fractionated Dipole Array"
N_DIPOLES = 8
DIPOLE_SETTINGS = {"length": 350,
                   "width": 10,
                   "gapwidth": 2,
                   "thickness": 0,
                   "matchingLEs": False}
FRACTIONATED_DIPOLE_CLASS = antennas.FractionatedDipole
ARRAY_WIDTH = 156  # in millimeters
ARRAY_HEIGHT = 190  # in millimeters
SPACER_THICKNESS = 10  # in millimeters

# phantom setup parameters
PHANTOM_NAME = "Head Phantom"
PHANTOM_SCALE_FACTOR = 0.90  # e.g. 1.05 for 5% increase, or 0.95 for 5% decrease

# calculate vertical adjustment factor for antennas based on scaling
ORIGINAL_PHANTOM_HEIGHT = 400  # Original height of the phantom in mm
ANTENNA_VERTICAL_ADJUSTMENT = ORIGINAL_PHANTOM_HEIGHT * (PHANTOM_SCALE_FACTOR) * 0.1
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

    # align phantom
    utils.align_head_phantom(model_name=PHANTOM_NAME)

    # scale phantom
    utils.scale_model(model_name=PHANTOM_NAME, scale_factor=PHANTOM_SCALE_FACTOR)

    # adjust antenna array height (z-coordinate) using utility function
    utils.translate_model(entity_name=ARRAY_NAME, translation_vector=(0, 0, ANTENNA_VERTICAL_ADJUSTMENT))

    # add spacers after moving the antenna array
    # Now, add spacers at the new position relative to the array
    frac_dipole_array.add_spacers(DIPOLE_SETTINGS["length"], DIPOLE_SETTINGS["width"] + 30, SPACER_THICKNESS)
    
    # Translate the spacers by the same vertical adjustment (this assumes spacers are a separate group)
    utils.translate_model(entity_name="Spacer Group", translation_vector=(0, 0, ANTENNA_VERTICAL_ADJUSTMENT))
