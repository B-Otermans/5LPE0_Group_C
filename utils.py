import XCoreModeling as xcm
import s4l_v1.model as model
from s4l_v1 import Scaling, Rotation, Translation
from s4l_v1.model import Vec3

import numpy as np


def clear_from_model(clear_list: list) -> None:
    for clear_entity in clear_list:
        exists = True
        while exists:
            entity_names = [ent.Name for ent in xcm.GetActiveModel().GetEntities()]
            if clear_entity in entity_names:
                for ent in xcm.GetActiveModel().GetEntities():
                    if ent.Name == clear_entity:
                        ent.Delete()
                        print(f"Deleted: {clear_entity}")
                        break
            else:
                exists = False


def scale_model(model_name: str, scale_factor: float) -> None:
    target_model = model.AllEntities()[model_name]
    # Define current scaling vector of target model
    target_scale = target_model.Transform.Scaling
    # Define inverse of current scaling vector
    reset_vector = model.Vec3(1/target_scale[0], 1/target_scale[1], 1/target_scale[2])
    # Turn the inverse scaling into a transform at target model's current coordinates
    reset_scaler = Scaling(reset_vector, target_model.Transform.Translation)
    # Apply inverse scaling transform, such that the target model returns to original scale
    target_model.ApplyTransform(reset_scaler)

    # Scale model from original size, to wanted scale
    scaler = Scaling(model.Vec3(scale_factor), target_model.Transform.Translation)
    target_model.ApplyTransform(scaler)


def align_head_phantom(model_name: str) -> None:
    phantom = model.AllEntities()[model_name]
    phantom.ApplyTransform(phantom.Transform.Inverse())
    rot_y = Rotation(1, np.pi)
    phantom.ApplyTransform(rot_y)
    rot_z = Rotation(2, 0.5*np.pi)
    phantom.ApplyTransform(rot_z)
    transl_z = Translation(Vec3(0, 0, -67))
    phantom.ApplyTransform(transl_z)


def align_duke() -> None:
    duke = model.AllEntities()["Duke"]
    mesh = model.AllEntities()["Bone Mesh System"]
    duke.ApplyTransform(mesh.Transform.Inverse())

    rot_z = Rotation(2, 0.5*np.pi)
    translation = Translation(Vec3(265, -145, -1720))

    duke.ApplyTransform(rot_z)
    duke.ApplyTransform(translation)


def translate_model(entity_name: str, translation_vector: tuple) -> None:
    """
    Translates a given model entity by the specified translation vector.

    :param entity_name: Name of the model entity to translate.
    :param translation_vector: Tuple (x, y, z) specifying the translation in millimeters.
    """
    # Fetch the entity from the model
    entity = model.AllEntities()[entity_name]
    # Create a translation object
    translation = Translation(Vec3(*translation_vector))
    # Apply the translation to the entity
    entity.ApplyTransform(translation)
