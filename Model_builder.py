"""
File: Model_builder.py
Author: Koen Vat  k.vat@student.tue.nl
Date: 06-12-2023

This file can be used to generate antenna models and simulations in Sim4life. 
The file will generate a Cubic phantom, dielectric spacer and Dipole antenna.
If an object called Phantom is already present in S4L, no new phantom will be created.


The functions to build the following antennas are included: 
    
    Fractionated (meandered) Dipole, 
    Plain Dipole 
    Lumped Dipole

After creating the models, the file will create Multiport, harmonic
simulations around a specified frequency for 1 antenna.

Uncomment the experiment below the function definitions for the desired antenna.
Users can specify: 
    
    *****Antenna parameters*****
    
    dipoletype:     Type of antenna. Included possibilities are: plain, lumped and fractionated
    L_list:         List of lengths in mm of the antennas.
    value_list =    List of lumped element values in case a lumped dipole is simulated.
    
    
    Thickness:      Thickness of the PEC of the antena. 
    matchingLEs:    Option to include a matching circuit to the antenna.   
                    If True, a series and parallel lumped element will be 
                    added to the source. 
                    Note: the lumped element values of this circuit have to be 
                    added manually in S4l.
    
    *****Simulation parameters*****        
        
    Freq_list: list of frequencies in MHz for the harmonic simulations

Sometimes modification to the functions need to be made. 
Examples are:   Simulation names  
                Larmor frequencis and B0 field strengths
                Phantom conductivity and relative permittivity (field strength dependent)
                Antenna and phantom grid sizes 

                
Please be carefull to stick to naming and unit conventions when making adjustments.
Any time you make an adjutment, save this file and reload it in S4l.
Do not change the file in S4L's scripter directly! This can lead to foulty overwrites.

If the same script is run twice, a second antenna will appear, but no second 
simulation will be made. In this case, delete the simulation and antenna that you want to recreate
 
"""

import s4l_v1.document as doc
import s4l_v1.model as mod
from s4l_v1.model import Vec3 as v3
from s4l_v1 import Unit
import s4l_v1.units as units
import numpy as np
import numpy
import s4l_v1.simulation.emfdtd as emfdtd
from s4l_v1 import ReleaseVersion

# Define the version to use for default values
ReleaseVersion.set_active(ReleaseVersion.version7_0)

#%%        ##############  Antenna Function definitions  ############## 

def MakePlainDipool(length, width = 10, x=0, y=0, gapwidth=2, thickness=0, matchingLEs=False):
	hl = length/2.0
	hgw = gapwidth/2.0
	hw = width/2.0
	arm1 = mod.CreateSolidBlock(v3(x,y-hw,-hgw),v3(x+thickness,y+hw,-hl))
	arm2 = mod.CreateSolidBlock(v3(x,y-hw,hgw),v3(x+thickness,y+hw,hl))
	copper = mod.Unite([arm1, arm2], 1)
	copper.Name = "Conductor "+ str(length)+ " plain"
	if matchingLEs:
		source = mod.CreatePolyLine([v3(x,y,0),v3(x,y,hgw)])
		source.Name = "source "+ str(length)+ " plain"
		sLE = mod.CreatePolyLine([v3(x,y,-hgw),v3(x,y,0)])
		sLE.Name = "seriesLE "+ str(length)+ " plain"
		pLE = mod.CreatePolyLine([v3(x,y-hw/2,-hgw),v3(x,y-hw/2,hgw)])
		pLE.Name = "parallelLE "+ str(length)+ " plain"
	else:
		source = mod.CreatePolyLine([v3(x,y,-hgw),v3(x,y,hgw)])
		source.Name = "source "+ str(length)+ " plain"
	
	antennagroup = mod.CreateGroup("Plain Dipole "+ str(length)+"mm")
	for elem in [copper, source]:
		antennagroup.Add(elem)
	if matchingLEs:
		for elem in [pLE, sLE]:
			antennagroup.Add(elem)	
	
	return antennagroup

def MakeLumpedDipool(length, width=10, x=0, y=0, gapwidth=2, thickness=0, matchingLEs=False):
    hl = length / 2.0
    hgw = gapwidth / 2.0
    hw = width / 2.0
    arm1 = mod.CreateSolidBlock(v3(x, y - hw, -hgw), v3(x + thickness, y + hw, -hl))
    arm2 = mod.CreateSolidBlock(v3(x, y - hw, hgw), v3(x + thickness, y + hw, hl))
    copper = mod.Unite([arm1, arm2], 1)
    copper.Name = "Conductor " + str(length) + " lumped"
    if matchingLEs:
        source = mod.CreatePolyLine([v3(x, y, 0), v3(x, y, hgw)])
        source.Name = "source " + str(length) + " lumped"
        sLE = mod.CreatePolyLine([v3(x, y, -hgw), v3(x, y, 0)])
        sLE.Name = "seriesLE " + str(length) + " lumped"
        pLE = mod.CreatePolyLine([v3(x, y - hw / 2, -hgw), v3(x, y - hw / 2, hgw)])
        pLE.Name = "parallelLE " + str(length) + " lumped"
    else:
        source = mod.CreatePolyLine([v3(x, y, -hgw), v3(x, y, hgw)])
        source.Name = "source " + str(length) + " lumped"

    counts = 1
    caps = []
    for z in hl * np.array([-2. / 3, -1. / 3, 1. / 3, 2. / 3]):

        subtractblok = mod.CreateSolidBlock(v3(x - 1, y - hw, z - 2), v3(x + 1, y + hw, z + 2))
        copper = mod.Subtract([copper, subtractblok])

        cap = mod.CreatePolyLine([v3(x, y, z - 2), v3(x, y, z + 2)])
        cap.Name = "capacitor " + str(counts) + " " + str(length)
        counts = counts + 1
        caps.append(cap)

    antennagroup = mod.CreateGroup("Lumped Dipole " + str(length) + "mm")

    for elem in [copper, source]:
        antennagroup.Add(elem)

    if matchingLEs:
        for elem in [pLE, sLE]:
            antennagroup.Add(elem)
def MakeFractionatedDipool(length, width=10, x=0, y=0, gapwidth=2, thickness=0, matchingLEs=False):
    hl = length / 2.0
    hgw = gapwidth / 2.0
    hw = width / 2.0
    arm1 = mod.CreateSolidBlock(v3(x, y - hw, -hgw), v3(x + thickness, y + hw, -hl))
    arm2 = mod.CreateSolidBlock(v3(x, y - hw, hgw), v3(x + thickness, y + hw, hl))
    copper = mod.Unite([arm1, arm2], 1)
    copper.Name = "Conductor " + str(length) + " fractionated"

    if matchingLEs:
        source = mod.CreatePolyLine([v3(x, y, 0), v3(x, y, hgw)])
        source.Name = "source " + str(length) + " fractionated"
        sLE = mod.CreatePolyLine([v3(x, y, -hgw), v3(x, y, 0)])
        sLE.Name = "seriesLE " + str(length) + " fractionated"
        pLE = mod.CreatePolyLine([v3(x, y - hw / 2, -hgw), v3(x, y - hw / 2, hgw)])
        pLE.Name = "parallelLE " + str(length) + " fractionated"
    else:
        source = mod.CreatePolyLine([v3(x, y, -hgw), v3(x, y, hgw)])
        source.Name = "source " + str(length) + " fractionated"

    for z in hl * np.array([-2. / 3, -1. / 3, 1. / 3, 2. / 3]):
    # for z in hl * np.array([-3. / 4,-2./4, -1. / 4, 1. / 4, 2. / 4,3./4]):        

        subtractblok = mod.CreateSolidBlock(v3(x - 1, y - hw, z - 6), v3(x + 1, y + hw, z + 6))
        copper = mod.Subtract([copper, subtractblok])
        pieces = []
        pieces.append(mod.CreateSolidBlock(v3(x, y + hw, z + 10), v3(x + thickness, y + hw + 6, z + 6)))
        pieces.append(mod.CreateSolidBlock(v3(x, y - hw, z - 6), v3(x + thickness, y - hw - 6, z - 10)))
        pieces.append(mod.CreateSolidBlock(v3(x, y - hw - 6, z + 2), v3(x + thickness, y + hw + 6, z - 2)))
        halfcircle1 = mod.CreateSolidTube(v3(x - 1, y + hw + 6, z + 4), v3(2, 0, 0), 6, 2)
        stukkie1 = mod.CreateSolidBlock(v3(x, y + hw + 6, z + 10), v3(x + thickness, y + hw + 12, z - 2))
        pieces.append(mod.Intersect([halfcircle1, stukkie1]))
        halfcircle2 = mod.CreateSolidTube(v3(x - 1, y - hw - 6, z - 4), v3(2, 0, 0), 6, 2)
        stukkie2 = mod.CreateSolidBlock(v3(x, y - hw - 6, z - 10), v3(x + thickness, y - hw - 12, z + 2))
        pieces.append(mod.Intersect([halfcircle2, stukkie2]))
        copper = mod.Unite([copper] + pieces)

    antennagroup = mod.CreateGroup("Fractionated Dipole " + str(length) + "mm")
    for elem in [copper, source]:
        antennagroup.Add(elem)
    if matchingLEs:
        for elem in [pLE, sLE]:
            antennagroup.Add(elem)

    return antennagroup

#%%      ##############  Model and simulation building functions  ############## 

def MakeModel(L,x=0, y=0, dipoletype='plain', thickness=0, matchingLEs=False):
    
	if not "phantom" in mod.AllEntities():
		phantom = mod.CreateSolidBlock(v3(-520,-250,-250), v3(-20,250,250))
		phantom.Name = "phantom"
	if not "spacer"+str(y) in mod.AllEntities():
		spacer = mod.CreateSolidBlock(v3(-20,-50+y,-150), v3(-10,50+y,150))
		spacer.Name = "spacer"+str(y)
	
	
	if dipoletype == 'Plain':
		antennagroup = MakePlainDipool(L, x=x, y=y, thickness=thickness, matchingLEs=matchingLEs)
	elif dipoletype == 'fractionated':
		antennagroup = MakeFractionatedDipool(L, x=x, y=y, thickness=thickness, matchingLEs=matchingLEs)
		
	elif dipoletype == "lumped":
		antennagroup = MakeLumpedDipool(L, x=x, y=y, thickness=thickness, matchingLEs=matchingLEs)
   

	return antennagroup



def MakeSIM_Multi(L,dipoletype = "plain", value = None,freq=298):
    
    #B0 definitions are mostly used for simulation naming and are frequency dependent
    if freq ==298:
        B0 = " 7T proton"
    elif freq ==596:
        B0 = " 14T proton"
    elif freq ==241:
        B0 = " 14T phosphorus"    
    else: 
        raise Exception("Undifined frequency. Values should be given in MHz. ")

    # Creating the simulation
    simulation = emfdtd.MultiportSimulation()
 

    if dipoletype == "Plain":
        simulation.Name = "Plain Dipole "+ str(L)+" mm"+ B0 + " block"
        
        entity_source = mod.AllEntities()["source "+str(L)+ " plain"]  
        entity_phantom = mod.AllEntities()["phantom"]
        entity__conductor = mod.AllEntities()["Conductor "+str(L)+ " plain"]  
    
    elif dipoletype == "fractionated":
        
        simulation.Name = "Fractionated Dipole "+ str(L) +" mm"+ B0 + "head"
        
        entity_source = mod.AllEntities()["source "+str(L)+ " fractionated"]  
        entity_phantom = mod.AllEntities()["phantom"]
        entity__conductor = mod.AllEntities()["Conductor "+str(L)+ " fractionated"]  
        
    elif dipoletype == "lumped":
        simulation.Name = "Lumped Dipole "+ str(L)+" mm"+" "+ str(value)+ B0 + " head"
        
        entity_source = mod.AllEntities()["source "+str(L)+ " lumped"]  
        entity_phantom = mod.AllEntities()["phantom"]
        entity__conductor = mod.AllEntities()["Conductor "+str(L)+ " lumped"]  
    
        entity_capacitor1 = mod.AllEntities()["capacitor 1 "+str(L)]  
        entity_capacitor2 = mod.AllEntities()["capacitor 2 "+str(L)] 
        entity_capacitor3 = mod.AllEntities()["capacitor 3 "+str(L)] 
        entity_capacitor4 = mod.AllEntities()["capacitor 4 "+str(L)]
        
    else: 
        raise Exception("Undifined antenna type. Please check spelling or modifiy simulation function")        
        
    # Editing SetupSettings "Setup
    setup_settings = simulation.SetupSettings
    setup_settings.GlobalAutoTermination = setup_settings.GlobalAutoTermination.enum.GlobalAutoTerminationUserDefined
    setup_settings.SimulationTime = 500, units.Periods
    
    # Adding a new MaterialSettings
    material_settings = emfdtd.MaterialSettings()
    components = [entity_phantom]
    material_settings.Name = "phantom"
	
    if freq ==298:
        material_settings.ElectricProps.Conductivity = 0.552035, Unit("S/m")
        material_settings.ElectricProps.RelativePermittivity = 51.954693
        simulation.Add(material_settings, components)
        
    elif freq ==596:
        material_settings.ElectricProps.Conductivity = 0.66, Unit("S/m")
        material_settings.ElectricProps.RelativePermittivity = 47.52
        simulation.Add(material_settings, components)
    
    elif freq ==241:
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
        if type(value)==str: 
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
              raise Exception("Wrong inter segment lumped element unit. Units should be nH for inductors or pF for capacitors")    
    
    
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
    automatic_grid_settings = [x for x in simulation.AllSettings if isinstance(x, emfdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
    simulation.RemoveSettings(automatic_grid_settings)
        
    
    # Adding a new ManualGridSettings
    manual_grid_settings = simulation.AddManualGridSettings([entity_phantom])
    manual_grid_settings.Name = "phantom_grid"
    manual_grid_settings.MaxStep = numpy.array([5.0, 5.0, 5.0]), units.MilliMeters
    manual_grid_settings.Resolution = numpy.array([10.0, 10.0, 10.0]), units.MilliMeters
    
    # Adding a new ManualGridSettings
    if dipoletype == "Plain" or dipoletype =="fractionated" or dipoletype == "meander" :
        manual_grid_settings = simulation.AddManualGridSettings([entity__conductor, entity_source])
    elif dipoletype == "lumped":
        manual_grid_settings = simulation.AddManualGridSettings([entity__conductor, entity_source, entity_capacitor1, entity_capacitor2, entity_capacitor3, entity_capacitor4])
    
    else: 
        raise Exception("Undifined antenna type in gridsettings. Please check spelling or modifiy simulation function")    
        
    manual_grid_settings.Name = "antenna_grid"
    manual_grid_settings.MaxStep = numpy.array([1, 1, 1]), units.MilliMeters
    manual_grid_settings.Resolution = numpy.array([0.05, 0.05, 0.05]), units.MilliMeters
    
    # Editing AutomaticVoxelerSettings "Automatic Voxeler Settings
    automatic_voxeler_settings = [x for x in simulation.AllSettings if isinstance(x, emfdtd.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
    if dipoletype == "Plain" or dipoletype =="fractionated" or dipoletype == "meander":
        components = [entity__conductor, entity_source, entity_phantom]
    elif dipoletype == "lumped":
        components = [entity__conductor, entity_source, entity_capacitor1, entity_capacitor2, entity_capacitor3, entity_capacitor4, entity_phantom]
        
    else: 
        raise Exception("Undifined antenna type in gridsettings. Please check spelling or modifiy simulation function")    
    
    simulation.Add(automatic_voxeler_settings, components)
    
    
    # Editing SolverSettings "Solver
    solver_settings = simulation.SolverSettings
    solver_settings.Kernel = solver_settings.Kernel.enum.Cuda
    
    # Update the materials with the new frequency parameters
    simulation.UpdateAllMaterials()
    
    # Update the grid with the new parameters
    simulation.UpdateGrid()
    
    # Add the simulation to the UI
    doc.AllSimulations.Add( simulation )


#%%  ##############  Antenna experiments ############## 

def Run_experiments(case):
    
    if case == 0:
        """Plain dipole experiment"""
    
        dipoletype = 'Plain' 
        L_list = [300]
        value_list = [None]
        thickness=0
        matchingLEs = False
        
        freq_list = [596]       #Larmor frequencies for H and P at 14T
    
    
    if case == 1:
         
        """Lumped dipole experiment"""       
            
        dipoletype = 'lumped'
        L_list = [300]
        value_list=["0.5pF","1pF","2pF","5pF","10pF","20nH","40nH","60nH","80nH","100nH"]   # Intersegment lumped element values for capacitors and/or inductors
        thickness=0
        matchingLEs = False
        
        freq_list = [596]
        
    if case == 2:
    
        """Fractionated (meandered) dipole experiment"""   
        
        dipoletype = 'fractionated' 
        L_list = [450]
        value_list=[None]
        thickness=0
        matchingLEs = False
        
        
        freq_list = [298]
        
    for L in L_list:
       
        antennagroup = MakeModel(L, dipoletype = dipoletype, thickness=thickness, matchingLEs=matchingLEs)
    
        for freq in freq_list:
            for value in value_list:
                
                MakeSIM_Multi(L=L,dipoletype=dipoletype, value = value,freq=freq)


#%%  ##############  Create the chosen experiments  ############## 
# for i in range(3):
#     	Run_experiments(i)

import XCoreModeling as xcm
xcm.GetActiveModel().Clear()                
Run_experiments(2)

print("done")