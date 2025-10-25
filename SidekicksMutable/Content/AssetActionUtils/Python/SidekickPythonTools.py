# SidekickPythonTools.py
import unreal

BAD_BONES = ["transform1", "transform2", "transform3"]

def _log(msg): unreal.log("[FixSyntySidekickSkeleton] " + msg)

def _as_name(x) -> unreal.Name:
    return x if isinstance(x, unreal.Name) else unreal.Name(str(x))

def _children_of(mod: unreal.SkeletonModifier, bone: unreal.Name, all_bones: list[unreal.Name]) -> list[unreal.Name]:
    """Return direct children of 'bone' from all_bones."""
    get_parent = mod.get_parent_name
    bone = _as_name(bone)
    # 'all_bones' should be Names; don't reconvert on every iteration
    return [b for b in all_bones if get_parent(b) == bone]

def _has_parent(mod: unreal.SkeletonModifier, bone: unreal.Name) -> bool:
    """True if bone has a valid parent (i.e., not NAME_None)."""
    p = mod.get_parent_name(_as_name(bone))
    # In UE, NAME_None is a valid Name object; treat falsy/None/NAME_None as no parent
    return bool(p) and str(p) != "None"

def _depth_of(mod: unreal.SkeletonModifier, bone: unreal.Name) -> int:
    """Depth from root; root has depth 0."""
    depth = 0
    cur = _as_name(bone)
    while _has_parent(mod, cur):
        cur = mod.get_parent_name(cur)
        depth += 1
    return depth

def FixSyntySidekickSkeleton_transform_bones(asset) -> bool:
    """
    asset - Skeletal Mesh whose skeleton is changed
    Returns True if any changes were made.
    """

    # Use SkeletonModifier bound to this mesh (so we can edit bone hierarchy)
    skel_mod = unreal.SkeletonModifier()
    mesh_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
    mesh_loaded = unreal.EditorAssetLibrary.load_asset(mesh_path)
    skel_mod.set_skeletal_mesh(mesh_loaded)
    bones = skel_mod.get_all_bone_names()
    _log(f"{bones}")
    bone_names_str = {str(b) for b in bones}

    # Only act on BAD_BONES that actually exist
    present_names: list[unreal.Name] = [_as_name(b) for b in BAD_BONES if b in bone_names_str]
    if not present_names:
        _log(f"{asset.get_name()}: no transform# bones → skip.")
        return False

    unreal.log(f"INFO: The provided skeletal mesh {asset.get_name()} has transform# bones. Processing.")
    #return True # Debug escape to check script call

    # If a 'bad' bone is parented under another 'bad', do deepest first
    present_names.sort(key=lambda b: _depth_of(skel_mod, b), reverse=True)
    # Pre-build a set for quick membership checks (skip reparent if child also to be removed)
    to_remove_set = set(present_names)


    changed = False
    with unreal.ScopedEditorTransaction("Fix SYNTY transform bones (UE5.6)"):
        for bad in present_names:
            if not _has_parent(skel_mod, bad):
                unreal.log_warning(f"{asset.get_name()}: '{str(bad)}' has no parent, skipping.")
                continue

            parent = skel_mod.get_parent_name(bad)
            bad_local = skel_mod.get_bone_transform(bad, False)  # local space of 'bad' relative to its parent
            # Collect BEFORE any hierarchy edits
            children = _children_of(skel_mod, bad, bones)

            # Reparent each child that is NOT also being removed
            for child in children:
                if child in to_remove_set:
                    # Will be handled when its turn comes
                    continue

                child_local = skel_mod.get_bone_transform(child, False)  # local of child relative to 'bad'

                # Compose to get child's local relative to 'parent':
                # new_local = child_local ∘ bad_local
                # UE rule of thumb: A * B applies B then A, so child_local * bad_local is correct here.
                new_local = child_local * bad_local

                skel_mod.parent_bone(child, parent)                 # now child is under 'parent'
                skel_mod.set_bone_transform(child, new_local, True)  # True = local-space transform
                changed = True

            # Finally remove the 'bad' bone
            skel_mod.remove_bone(bad, True)
            _log(f"{asset.get_name()}: removed {str(bad)}, reparented {[str(c) for c in children]} → {str(parent)}")
            changed = True

        if changed:
            # Save both mesh and skeleton explicitly (don’t rely on implicit save via reference)
            skel_mod.commit_skeleton_to_skeletal_mesh()
            unreal.EditorAssetLibrary.save_asset(mesh_path)

    return changed