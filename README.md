# 5LPE0_Group_C
## This Repository
This repository contains the code used in the research report "An Optimal Fractionated Dipole Based Antenna for MRI Brain Imaging at 7T" for the course "Electromagnetic fields in MRI: theory, simulations, building and testing (5PLE0)" of the Technical University Eindhoven. This Readme functions as a concise documentation of the files used for the simulations and data analysis used in this project.
## Reproduction of results
To reproduce the results presented in the report, one can follow this scheme:

In Sim4Life:
1.	_Load the Duke cV3-1 human model._
2.	**setup_controls_duke.py**: run this file with the desired parameters for the fractionated dipole array.
3.	**simulation_controls.py**: run this file with the desired parameters to build the simulation.
4.	_Manually add the Duke materials to the simulation and delete the area outside the bounding box._
5.	_Run the Sim4Life simulation._
6.	**analysis_controls.py**: run this file to combine the simulation results for manual inspection, and to extract the B1 fields of each antenna to .mat files.
7.	_Determine a slice along the Z-axis that will be the center of the region over which phase shimming will be optimized._

In MATLAB:
8.	**phase_optimiser.m**: supply the correct filenames that contain antenna data, the starting phases for each antenna, and the center slice that will determine the region for which B1+ homogeneity will be optimized. Then run this file to find optimal phases for phase shimming to achieve homogeneity.
9.	_Note the resulting phases to use them for plotting the new field._
10.	**Plot_S4L_2D.m**: supply the correct filenames and the wanted phases, then run this file to plot chosen slices along chosen planes.
 ## File Descriptions
The files are not ordered in folders, but they could be categorized into the following groups.
 ### Sim4Life Scripts
These files must be run in Sim4Life and can be subdivided into:
**Control scripts**: These scripts split up three phases of Sim4Life simulation such that they can be run separately.
- setup_controls.py: loading in and setting up antennas and arrays for simulation on a simple model.
- setup_controls_duke.py: loading in and setting up antennas and arrays for simulation on the Duke model.
- simulation_controls.py: set simulation settings, instantiate and run simulation.
- analysis_controls.py: run analysis pipeline for simulation results combination and extraction.
- Model_builder.py: contains source code used to model fractionated dipole antennas in Sim4Life, courtesy of Koen Vat.
**Modules**: Files containing functions and classes for running fractionated dipole antenna and antenna array experiments in Sim4Life.
- utils.py: helper functions (updating modules, clearing entity groups from model).
- antennas.py: antenna and antenna array classes and functions.
- simulate.py: simulation classes and functions.
### MATLAB Scripts
These are a couple scripts that were used phase shimming optimization as well as data visualization and interpretation.
- phase_optimiser.m: runs the algorithm that finds optimal phases for B1+ homogeneity.
- Plot_S4L_2D.m: plotting function for B1+ fields.
- calcMSE_plotstrengthvsMSE.m: plot field MSE vs B1+ field strength (not used in report).
