import s4l_v1.model as model
from s4l_v1.model import Vec3
from s4l_v1 import Rotation, Translation

import numpy as np


class FractionatedDipole:

    def __init__(self, length, name="Fractionated Dipole", width=10, x=0, y=0, gapwidth=2, thickness=0,
                 matchingLEs=False):

        self.element_group = model.CreateGroup(name)
        self.name = name

        hl = length / 2.0
        hgw = gapwidth / 2.0
        hw = width / 2.0
        arm1 = model.CreateSolidBlock(Vec3(x, y - hw, -hgw), Vec3(x + thickness, y + hw, -hl))
        arm2 = model.CreateSolidBlock(Vec3(x, y - hw, hgw), Vec3(x + thickness, y + hw, hl))
        self.copper = model.Unite([arm1, arm2], 1)
        self.copper.Name = "Conductor"

        if matchingLEs:
            self.source = model.CreatePolyLine([Vec3(x, y, 0), Vec3(x, y, hgw)])
            self.source.Name = "Source"
            self.sLE = model.CreatePolyLine([Vec3(x, y, -hgw), Vec3(x, y, 0)])
            self.sLE.Name = "SeriesLE"
            self.pLE = model.CreatePolyLine([Vec3(x, y - hw / 2, -hgw), Vec3(x, y - hw / 2, hgw)])
            self.pLE.Name = "ParallelLE"
        else:
            self.source = model.CreatePolyLine([Vec3(x, y, -hgw), Vec3(x, y, hgw)])
            self.source.Name = "Source"
            self.sLE = None
            self.pLE = None

        # for z in hl * np.array([-3. / 4,-2./4, -1. / 4, 1. / 4, 2. / 4,3./4]):
        for z in hl * np.array([-2. / 3, -1. / 3, 1. / 3, 2. / 3]):
            subtractblok = model.CreateSolidBlock(Vec3(x - 1, y - hw, z - 6), Vec3(x + 1, y + hw, z + 6))
            self.copper = model.Subtract([self.copper, subtractblok])
            pieces = []
            pieces.append(model.CreateSolidBlock(Vec3(x, y + hw, z + 10), Vec3(x + thickness, y + hw + 6, z + 6)))
            pieces.append(model.CreateSolidBlock(Vec3(x, y - hw, z - 6), Vec3(x + thickness, y - hw - 6, z - 10)))
            pieces.append(model.CreateSolidBlock(Vec3(x, y - hw - 6, z + 2), Vec3(x + thickness, y + hw + 6, z - 2)))
            halfcircle1 = model.CreateSolidTube(Vec3(x - 1, y + hw + 6, z + 4), Vec3(2, 0, 0), 6, 2)
            stukkie1 = model.CreateSolidBlock(Vec3(x, y + hw + 6, z + 10), Vec3(x + thickness, y + hw + 12, z - 2))
            pieces.append(model.Intersect([halfcircle1, stukkie1]))
            halfcircle2 = model.CreateSolidTube(Vec3(x - 1, y - hw - 6, z - 4), Vec3(2, 0, 0), 6, 2)
            stukkie2 = model.CreateSolidBlock(Vec3(x, y - hw - 6, z - 10), Vec3(x + thickness, y - hw - 12, z + 2))
            pieces.append(model.Intersect([halfcircle2, stukkie2]))
            self.copper = model.Unite([self.copper] + pieces)

        for elem in [self.copper, self.source]:
            self.element_group.Add(elem)
        if matchingLEs:
            for elem in [self.pLE, self.sLE]:
                self.element_group.Add(elem)

    def set_name(self, new_name):
        self.name = new_name
        self.element_group.Name = new_name


class ElipseArray:
    def __init__(self, name: str, n_antennas: int, antenna_parameters: dict, antenna_class=FractionatedDipole,
                 array_width: int = 240, array_height: int = 300):

        self.entity_group = model.EntityGroup()
        self.name = name

        # antenna angles start at 0.5pi such that the first antenna is above the face
        self.angles = np.linspace(0.5*np.pi, 2.5*np.pi, n_antennas, endpoint=False)
        self.coords_2D = np.vstack([np.array((array_width/2*np.cos(t), array_height/2*np.sin(t))) for t in self.angles])

        self.antenna_list = []
        self.entity_group.Name = self.name
        for i, coord in enumerate(self.coords_2D):
            antenna = antenna_class(**antenna_parameters)
            antenna.set_name(f"{antenna.name} {i+1}")
            self.antenna_list.append(antenna)
            self.entity_group.Add(antenna.element_group)

            # move antenna to the correct position and orientation
            rotation = Rotation(2, self.angles[i])
            translation = Translation(Vec3(coord[0], coord[1], 0))
            antenna.element_group.ApplyTransform(rotation)
            antenna.element_group.ApplyTransform(translation)

        print(f"Created: Elipse array with {n_antennas} '{antenna_class.__name__}' elements")

    def set_name(self, new_name):
        self.name = new_name
        self.entity_group.Name = new_name
