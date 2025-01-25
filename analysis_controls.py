import simulate
import imp

# force module updates
CUSTOM_MODULES = [simulate]
for module in CUSTOM_MODULES:
    imp.reload(module)

# extraction paramters
SIMULATION_NAME = "Fractionated Dipole Array simulation at 298MHz"
NORMALIZED_POWER = 8.0  # power in watts to be divided over antennas

# if-statement to only perform extraction when this file is run directly
if __name__ == "__main__":
    simulate.extract_multiport(simulation_name=SIMULATION_NAME, normalized_power=NORMALIZED_POWER)
    simulate.extract_singleports(simulation_name=SIMULATION_NAME, relative_path="EXPORTS")
