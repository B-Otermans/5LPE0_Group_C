import simulate
import utils


CUSTOM_MODULES = [simulate, utils]
SIMULATION_GROUPS = ["Fractionated Dipole Array"]


if __name__ == "__main__":
    # force module updates
    utils.update_modules(CUSTOM_MODULES)
    # run multiport simulation
    simulate.multiport_sim(L=250, dipoletype="fractionated", freq=298)
