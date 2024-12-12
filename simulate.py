import s4l_v1.simulation.emfdtd as emfdtd
import s4l_v1.document as document
import s4l_v1.units as units

import numpy as np


def multiport_sim(array, scan_object=None, frequency: int = 298, simulation_time: int = 500):

    # Instantiate the simulation
    simulation = emfdtd.MultiportSimulation()
    simulation.Name = f"{array.name} simulation at {frequency}MHz"

    # Editing SetupSettings
    setup_settings = simulation.SetupSettings
    setup_settings.GlobalAutoTermination = setup_settings.GlobalAutoTermination.enum.GlobalAutoTerminationUserDefined
    setup_settings.SimulationTime = simulation_time, units.Periods

    # Removing AutomaticGridSettings Automatic
    automatic_grid_settings = [x for x in simulation.AllSettings if isinstance(x, emfdtd.AutomaticGridSettings)
                               and x.Name == "Automatic"][0]
    simulation.RemoveSettings(automatic_grid_settings)

    # Editing AutomaticVoxelerSettings "Automatic Voxeler Settings
    automatic_voxeler_settings = [x for x in simulation.AllSettings if isinstance(x, emfdtd.AutomaticVoxelerSettings)
                                  and x.Name == "Automatic Voxeler Settings"][0]

    for antenna in array.antenna_list:
        # Add conductor MaterialSettings
        conductor_material_settings = emfdtd.MaterialSettings()
        conductor_material_settings.Name = f"PEC - {antenna.name}"
        conductor_material_settings.MaterialType = conductor_material_settings.MaterialType.enum.PEC
        simulation.Add(conductor_material_settings, antenna.copper)

        # Add EdgePortSettings
        edge_port_settings = emfdtd.EdgePortSettings()
        edge_port_settings.Name = f"Edge Port - {antenna.name}"
        edge_port_settings.CenterFrequency = frequency*1000000, units.Hz
        simulation.Add(edge_port_settings, antenna.source)

        # Add EdgeSensorSettings
        edge_sensor_settings = emfdtd.EdgeSensorSettings()
        edge_sensor_settings.Name = f"Edge Sensor - {antenna.name}"
        simulation.Add(edge_sensor_settings, antenna.source)

        # Add ManualGridSettings for antenna
        antenna_grid_settings = simulation.AddManualGridSettings([antenna.copper, antenna.source])
        antenna_grid_settings.Name = f"Antenna Grid - {antenna.name}"
        antenna_grid_settings.MaxStep = np.array([1, 1, 1]), units.MilliMeters
        antenna_grid_settings.Resolution = np.array([0.05, 0.05, 0.05]), units.MilliMeters

        # Add components to voxeler
        simulation.Add(automatic_voxeler_settings, [antenna.copper, antenna.source])

    # Add phantom settings
    if scan_object:
        # Add scan object MaterialSettings
        simulation.Add(scan_object.material, scan_object.components)

        # Add scan object ManualGridSettings
        phantom_grid_settings = simulation.AddManualGridSettings(scan_object)
        phantom_grid_settings.Name = "Phantom Grid"
        phantom_grid_settings.MaxStep = np.array([5.0, 5.0, 5.0]), units.MilliMeters
        phantom_grid_settings.Resolution = np.array([10.0, 10.0, 10.0]), units.MilliMeters

        # Add components to voxeler
        simulation.Add(automatic_voxeler_settings, scan_object)

    # Add OverallFieldSensor
    simulation.AddOverallFieldSensorSettings()

    # Editing SolverSettings "Solver
    solver_settings = simulation.SolverSettings
    solver_settings.Kernel = solver_settings.Kernel.enum.Cuda

    # Update the materials with the new frequency parameters
    simulation.UpdateAllMaterials()

    # Update the grid with the new parameters
    simulation.UpdateGrid()

    # Add the simulation to the UI
    document.AllSimulations.Add(simulation)
