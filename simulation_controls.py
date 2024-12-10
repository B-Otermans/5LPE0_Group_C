import simulate
import utils
import setup_controls


CUSTOM_MODULES = [simulate, utils, setup_controls]
SIMULATION_GROUPS = ["Fractionated Dipole Array"]


if __name__ == "__main__":
    # force module updates
    utils.update_modules(CUSTOM_MODULES)
    # run multiport simulation
    simulate.multiport_sim(setup_controls.frac_dipole_array, frequency=298)
