import simulate
import utils
import setup_controls_duke
import imp


# force module updates
CUSTOM_MODULES = [simulate, utils, setup_controls_duke]
for module in CUSTOM_MODULES:
    imp.reload(module)

# simulation parameters
PHANTOM_NAME = ""  # Duke is not incorperated in sim function, empty string is the same as omitting phantom name
USE_CUDA = True
BOUNDING_BOX = "Bounding Box"

# Grid padding settings set-up
top_padding = 200
bottom_padding = 200
top_padding = top_padding * setup_controls_duke.PHANTOM_SCALE_FACTOR
bottom_padding = bottom_padding * setup_controls_duke.PHANTOM_SCALE_FACTOR

# grid settings in millimeters
GRID_SETTINGS = {"antenna_grid_max_step": 1.0,
                 "antenna_grid_resolution": 0.05,
                 "phantom_grid_max_step": 3.0,
                 "phantom_grid_resolution": 10.0
                 }

# if-statement to only perform simulation when this file is run directly
if __name__ == "__main__":
    # run multiport simulation
    simulate.multiport_sim(array=frac_dipole_array,
                           phantom_name=PHANTOM_NAME,
                           bounding_box=BOUNDING_BOX,
                           cuda_kernel=USE_CUDA,
                           top_padding=top_padding,
                           bottom_padding=bottom_padding,
                           **GRID_SETTINGS)
