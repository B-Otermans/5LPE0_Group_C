import simulate
import utils
import setup_controls
import imp

# force module updates
CUSTOM_MODULES = [simulate, utils, setup_controls]
for module in CUSTOM_MODULES:
    imp.reload(module)

SIMULATION_GROUPS = ["Fractionated Dipole Array"]


if __name__ == "__main__":
    # run multiport simulation
    simulate.multiport_sim(frac_dipole_array, frequency=298)
