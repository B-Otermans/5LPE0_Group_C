import simulate
import utils
import imp

# force module updates
CUSTOM_MODULES = [simulate, utils]
for module in CUSTOM_MODULES:
    imp.reload(module)

# simulation parameters
PHANTOM_NAME = "Head Phantom"
USE_CUDA = True
# grid settings in millimeters
GRID_SETTINGS = {"antenna_grid_max_step": 5.0,
                 "antenna_grid_resolution": 0.05,
                 "phantom_grid_max_step": 5.0,
                 "phantom_grid_resolution": 10.0
                 }

# if-statement to only perform simulation when this file is run directly
if __name__ == "__main__":
    # run multiport simulation
    simulate.multiport_sim(array=frac_dipole_array,
                           phantom_name=PHANTOM_NAME,
                           frequency=298,
                           cuda_kernel=USE_CUDA,
                           **GRID_SETTINGS
                           )
