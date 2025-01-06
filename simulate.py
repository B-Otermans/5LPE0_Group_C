import s4l_v1.simulation.emfdtd as emfdtd
import s4l_v1.analysis as analysis
import s4l_v1.document as document
import s4l_v1.units as units
import s4l_v1.model as model
from s4l_v1 import Unit
from s4l_v1 import ArchivingOptions
from s4l_v1.model import Vec3 as v3
from s4l_v1 import Rotation, Translation
import utils
import numpy as np


def multiport_sim(array, phantom_name: str = "", frequency: int = 298, simulation_time: int = 500,
                  cuda_kernel: bool = False,
                  antenna_grid_max_step: float = 5.0, antenna_grid_resolution: float = 0.05,
                  phantom_grid_max_step: float = 5.0, phantom_grid_resolution: float = 10.0, use_box: bool = False) -> None:
    # Instantiate the simulation



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
    #Changing padding global grid
    global_grid_settings = simulation.GlobalGridSettings
    global_grid_settings.PaddingMode = global_grid_settings.PaddingMode.enum.Manual
    global_grid_settings.BottomPadding = numpy.array([bottom_padding, bottom_padding, bottom_padding]), units.MilliMeters
    global_grid_settings.TopPadding = numpy.array([top_padding, top_padding, top_padding]), units.MilliMeters

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
        antenna_grid_settings.MaxStep = np.array([antenna_grid_max_step] * 3), units.MilliMeters
        antenna_grid_settings.Resolution = np.array([antenna_grid_resolution] * 3), units.MilliMeters

        # Add components to voxeler
        simulation.Add(automatic_voxeler_settings, [antenna.copper, antenna.source])

    # Add phantom settings
    if phantom_name:
        phantom = model.AllEntities()[phantom_name]
        # Add scan object MaterialSettings
        phantom_material_settings = emfdtd.MaterialSettings()
        phantom_material_settings.ElectricProps.Conductivity = 0.552035, Unit("S/m")
        phantom_material_settings.ElectricProps.RelativePermittivity = 51.954693
        phantom_material_settings.Name = "Phantom"

        simulation.Add(phantom_material_settings, [phantom])

        # Add scan object ManualGridSettings
        phantom_grid_settings = simulation.AddManualGridSettings([phantom])
        phantom_grid_settings.Name = "Phantom Grid"
        phantom_grid_settings.MaxStep = np.array([phantom_grid_max_step] * 3), units.MilliMeters
        phantom_grid_settings.Resolution = np.array([phantom_grid_resolution] * 3), units.MilliMeters

        # Add components to voxeler
        simulation.Add(automatic_voxeler_settings, [phantom])

    if use_box:
        start_point = v3(0, 0, 0)  # Adjust starting point if needed
        end_point = v3(start_point[0] + BOX_DIMENSIONS[0], 
					start_point[1] + BOX_DIMENSIONS[1], 
					start_point[2] + BOX_DIMENSIONS[2])

        BOX = model.CreateWireBlock(start_point, end_point)
        BOX.Name = 'BOX'
        translation = Translation(v3(-97.5,-125,-150))
        BOX.ApplyTransform(translation)
        utils.scale_model(model_name='BOX', scale_factor=PHANTOM_SCALE_FACTOR)

        #BOX_material_settings = emfdtd.MaterialSettings()
        #BOX_material_settings.ElectricProps.Conductivity = 0, Unit("S/m")
        #BOX_material_settings.MassDensity = 1.205
        #BOX_material_settings.ElectricProps.RelativePermittivity = 1
        #BOX_material_settings.Name = "Box"
        #simulation.Add(BOX_material_settings, [BOX])

        BOX_grid_settings = simulation.AddManualGridSettings([BOX])
        BOX_grid_settings.Name = "Box Grid"
        BOX_grid_settings.MaxStep = np.array([phantom_grid_max_step] * 3), units.MilliMeters
        BOX_grid_settings.Resolution = np.array([phantom_grid_resolution] * 3), units.MilliMeters

        automatic_voxeler_settings = emfdtd.AutomaticVoxelerSettings()
        simulation.Add(automatic_voxeler_settings, [BOX])


    # Add OverallFieldSensor
    OverallFieldSensorSettings = simulation.AddOverallFieldSensorSettings()
    simulation.Add(OverallFieldSensorSettings,[BOX])
    # Editing SolverSettings "Solver
    if cuda_kernel:
        solver_settings = simulation.SolverSettings
        solver_settings.Kernel = solver_settings.Kernel.enum.Cuda

    # Update the materials with the new frequency parameters
    simulation.UpdateAllMaterials()

    # Update the grid with the new parameters
    simulation.UpdateGrid()

    # Add the simulation to the UI
    document.AllSimulations.Add(simulation)


def extract_multiport(simulation_name: str, normalized_power: int = 0):
    # Add an EmMultiPortSimulationExtractor
    simulation = document.AllSimulations[simulation_name]
    em_multi_port_simulation_extractor = simulation.Results()

    # Add an EmMultiPortSimulationCombiner
    inputs = [output for output in em_multi_port_simulation_extractor.Outputs]
    em_multi_port_simulation_combiner = analysis.extractors.EmMultiPortSimulationCombiner(inputs=inputs)

    phases = np.linspace(0, 360, len(inputs), endpoint=False)
    for i, channel in enumerate(em_multi_port_simulation_combiner.GetChannelWeights()):
        power = normalized_power/len(inputs) if normalized_power else 0
        em_multi_port_simulation_combiner.SetChannelWeight(channel, power, phases[i])

    em_multi_port_simulation_combiner.UpdateAttributes()
    em_multi_port_simulation_combiner.Update()

    document.AllAlgorithms.Add(em_multi_port_simulation_combiner)

def extract_singleports(simulation_name: str, relative_path: str):
    #Prepare new path for exports
    path = document.FilePath
    path = path.split('\\')[:-1]
    path = "\\".join(path)
    newpath = path + '\\' + relative_path
    print("Export path: " + newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    #Extract sensors and export in relative path
    simulation = document.AllSimulations[simulation_name]
    em_multiport_simulation_extractor = simulation.Results()
    sensors = [s for s in em_multiport_simulation_extractor]
    for i, s in enumerate(sensors):
        em_sensor = s["Overall Field"]
        document.AllAlgorithms.Add(em_sensor)
        inputs = [em_sensor.Outputs["B1(x,y,z,f0)"]]
        viewer = analysis.viewers.SliceFieldViewer(inputs=inputs)
        document.AllAlgorithms.Add(viewer)
        exporter = analysis.exporters.MatlabExporter(inputs=inputs)
        exporter.FileName = newpath + "\\sensor_" + str(i) + ".mat"
        exporter.UpdateAttributes()
        exporter.Update()
        document.AllAlgorithms.Add(exporter)



