import simulate
import utils
import setup_controls_duke
import imp

# Force update scaling factor
imp.reload(setup_controls_duke)

# force module updates
CUSTOM_MODULES = [simulate, utils]
for module in CUSTOM_MODULES:
    imp.reload(module)

# simulation parameters
PHANTOM_NAME = ""
USE_BOX = True
USE_CUDA = True

# Grid padding settings set-up
top_padding = 200
bottom_padding = 200
top_padding = top_padding * setup_controls.PHANTOM_SCALE_FACTOR
bottom_padding = bottom_padding * setup_controls.PHANTOM_SCALE_FACTOR

# grid settings in millimeters
GRID_SETTINGS = {"antenna_grid_max_step": 0.5,
                 "antenna_grid_resolution": 0.05,
                 "phantom_grid_max_step": 1.0,
                 "phantom_grid_resolution": 10.0
                 }

# if-statement to only perform simulation when this file is run directly
if __name__ == "__main__":
    # run multiport simulation
    simulate.multiport_sim(array=frac_dipole_array,
                           phantom_name=PHANTOM_NAME,
                           use_box=USE_BOX,
                           cuda_kernel=USE_CUDA,
                           top_padding=top_padding,
                           bottom_padding=bottom_padding,
                           PHANTOM_SCALE_FACTOR=setup_controls_duke.PHANTOM_SCALE_FACTOR,
                           BOX_DIMENSIONS=setup_controls_duke.BOX_DIMENSIONS,
                           **GRID_SETTINGS)
