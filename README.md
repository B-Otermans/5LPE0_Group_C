# 5LPE0_Group_C
 
 ### Control scripts
Control scripts split up three phases such that they can be run separately:

    - model_controls: loading in and setting up antennas and arrays
    - simulation_controls: set simulation settings, instantiate and run simulation
    - analysis_controls: run analysis pipeline

### Modules
Files containing functions and classes for running antenna and antenna array experiments in Sim4Life:

    - utils: helper functions (updating modules, clearing entity groups from model)
    - antennas: antenna and antenna array classes and functions
    - simulate: simulation classes and functions
