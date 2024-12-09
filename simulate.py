import s4l_v1.model as model
import s4l_v1.simulation.emfdtd as emfdtd
import s4l_v1.document as document
import s4l_v1.units as units
from s4l_v1 import Unit

import numpy as np


def multiport_sim(antenna_group, scan_object=None, freq=298):

    # Instantiate the simulation
    simulation = emfdtd.MultiportSimulation()
    simulation.Name = f"{antenna_group.Name} simulation at {freq}MHz"

    for antenna in antenna_group:
        source_entity = [entity for entity in antenna.Entities if entity.Name == "Source"][0]
        conductor_entity = [entity for entity in antenna.Entities if entity.Name == "Conductor"][0]

    if dipoletype == "Plain":
        simulation.Name = f"Plain Dipole {L}mm {B0} block"

        entity_source = model.AllEntities()[f"source {L} plain"]
        entity_phantom = model.AllEntities()["phantom"]
        entity__conductor = model.AllEntities()[f"Conductor {L} plain"]

    elif dipoletype == "fractionated":
        simulation.Name = f"Fractionated Dipole {L}mm {B0} head"

        entity_source = model.AllEntities()[f"source {L} fractionated"]
        entity_phantom = model.AllEntities()["phantom"]
        entity__conductor = model.AllEntities()[f"Conductor {L} fractionated"]

    elif dipoletype == "lumped":
        simulation.Name = f"Lumped Dipole {L}mm {value} {B0} head"

        entity_source = model.AllEntities()[f"source {L} lumped"]
        entity_phantom = model.AllEntities()["phantom"]
        entity__conductor = model.AllEntities()[f"Conductor {L} lumped"]

        entity_capacitor1 = model.AllEntities()[f"capacitor 1 {L}"]
        entity_capacitor2 = model.AllEntities()[f"capacitor 2 {L}"]
        entity_capacitor3 = model.AllEntities()[f"capacitor 3 {L}"]
        entity_capacitor4 = model.AllEntities()[f"capacitor 4 {L}"]

    else:
        raise Exception("Undifined antenna type. Please check spelling or modelifiy simulation function")

    # Editing SetupSettings "Setup
    setup_settings = simulation.SetupSettings
    setup_settings.GlobalAutoTermination = setup_settings.GlobalAutoTermination.enum.GlobalAutoTerminationUserDefined
    setup_settings.SimulationTime = 500, units.Periods

    # Adding a new MaterialSettings
    material_settings = emfdtd.MaterialSettings()
    components = [entity_phantom]
    material_settings.Name = "phantom"

    if freq == 298:
        material_settings.ElectricProps.Conductivity = 0.552035, Unit("S/m")
        material_settings.ElectricProps.RelativePermittivity = 51.954693
        simulation.Add(material_settings, components)

    elif freq == 596:
        material_settings.ElectricProps.Conductivity = 0.66, Unit("S/m")
        material_settings.ElectricProps.RelativePermittivity = 47.52
        simulation.Add(material_settings, components)

    elif freq == 241:
        material_settings.ElectricProps.Conductivity = 0.46, Unit("S/m")
        material_settings.ElectricProps.RelativePermittivity = 38
        simulation.Add(material_settings, components)

    else:
        raise Exception("Undifined frequency. Values should be given in MHz.")

    # Adding a new MaterialSettings
    material_settings = emfdtd.MaterialSettings()
    components = [entity__conductor]
    material_settings.Name = "PEC"
    material_settings.MaterialType = material_settings.MaterialType.enum.PEC
    simulation.Add(material_settings, components)

    # Adding a new EdgePortSettings
    edge_port_settings = emfdtd.EdgePortSettings()
    components = [entity_source]
    edge_port_settings.CenterFrequency = freq*1000000, units.Hz
    simulation.Add(edge_port_settings, components)

    if dipoletype == "lumped":
        if isinstance(value, str):
            if value[-2:] == "pF":
                lumped_element_settings = emfdtd.LumpedElementSettings()
                components = [entity_capacitor1, entity_capacitor2, entity_capacitor3, entity_capacitor4]
                lumped_element_settings.Type = lumped_element_settings.Type.enum.Capacitor
                lumped_element_settings.Capacitance = float(value[0:-2])/1000000000000, units.Farads
                simulation.Add(lumped_element_settings, components)

            elif value[-2:] == "nH":
                lumped_element_settings = emfdtd.LumpedElementSettings()
                components = [entity_capacitor1, entity_capacitor2, entity_capacitor3, entity_capacitor4]
                lumped_element_settings.Type = lumped_element_settings.Type.enum.Inductor
                lumped_element_settings.Inductance = float(value[0:-2])/1000000000, units.Henrys
                simulation.Add(lumped_element_settings, components)

            else:
                raise Exception("Wrong inter segment lumped element unit. "
                                "Units should be nH for inductors or pF for capacitors")

    # Adding a new EdgeSensorSettings
    edge_sensor_settings = emfdtd.EdgeSensorSettings()
    components = [entity_source]
    edge_sensor_settings.Name = "Edge Sensor Settings 1"
    simulation.Add(edge_sensor_settings, components)

    if dipoletype == "lumped":
        edge_sensor_settings = emfdtd.EdgeSensorSettings()
        components = [entity_capacitor1, entity_capacitor2, entity_capacitor3, entity_capacitor4]
        edge_sensor_settings.Name = "Edge Sensor Settings 4"
        simulation.Add(edge_sensor_settings, components)

    # Removing AutomaticGridSettings Automatic
    automatic_grid_settings = [x for x in simulation.AllSettings if isinstance(x, emfdtd.AutomaticGridSettings)
                               and x.Name == "Automatic"][0]
    simulation.RemoveSettings(automatic_grid_settings)

    # Adding a new ManualGridSettings
    manual_grid_settings = simulation.AddManualGridSettings([entity_phantom])
    manual_grid_settings.Name = "phantom_grid"
    manual_grid_settings.MaxStep = np.array([5.0, 5.0, 5.0]), units.MilliMeters
    manual_grid_settings.Resolution = np.array([10.0, 10.0, 10.0]), units.MilliMeters

    # Adding a new ManualGridSettings
    if dipoletype in ["Plain", "fractionated", "meander"]:
        manual_grid_settings = simulation.AddManualGridSettings([entity__conductor, entity_source])
    elif dipoletype == "lumped":
        manual_grid_settings = simulation.AddManualGridSettings([entity__conductor, entity_source, entity_capacitor1,
                                                                 entity_capacitor2, entity_capacitor3,
                                                                 entity_capacitor4])

    else:
        raise Exception("Undifined antenna type in gridsettings. "
                        "Please check spelling or modelifiy simulation function")

    manual_grid_settings.Name = "antenna_grid"
    manual_grid_settings.MaxStep = np.array([1, 1, 1]), units.MilliMeters
    manual_grid_settings.Resolution = np.array([0.05, 0.05, 0.05]), units.MilliMeters

    # Editing AutomaticVoxelerSettings "Automatic Voxeler Settings
    automatic_voxeler_settings = [x for x in simulation.AllSettings if isinstance(x, emfdtd.AutomaticVoxelerSettings)
                                  and x.Name == "Automatic Voxeler Settings"][0]
    if dipoletype in ["Plain", "fractionated", "meander"]:
        components = [entity__conductor, entity_source, entity_phantom]
    elif dipoletype == "lumped":
        components = [entity__conductor, entity_source, entity_capacitor1, entity_capacitor2, entity_capacitor3,
                      entity_capacitor4, entity_phantom]

    else:
        raise Exception("Undifined antenna type in gridsettings. "
                        "Please check spelling or modelifiy simulation function")

    simulation.Add(automatic_voxeler_settings, components)

    # Editing SolverSettings "Solver
    solver_settings = simulation.SolverSettings
    solver_settings.Kernel = solver_settings.Kernel.enum.Cuda

    # Update the materials with the new frequency parameters
    simulation.UpdateAllMaterials()

    # Update the grid with the new parameters
    simulation.UpdateGrid()

    # Add the simulation to the UI
    document.AllSimulations.Add(simulation)
