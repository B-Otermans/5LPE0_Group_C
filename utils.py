import XCoreModeling as xcm
import imp


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


def update_modules(module_list: list) -> None:
    for module in module_list:
        imp.reload(module)
