import simulate
import imp

# force module updates
CUSTOM_MODULES = [simulate]
for module in CUSTOM_MODULES:
    imp.reload(module)

# extraction paramters
SIMULATION_NAME = "Fractionated Dipole Array simulation at 298MHz"

# if-statement to only perform extraction when this file is run directly
if __name__ == "__main__":
    simulate.extract_singleports(simulation_name=SIMULATION_NAME, relative_path="EXPORTS")
