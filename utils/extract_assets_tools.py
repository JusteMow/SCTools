import os
import shutil
import states.states as states
import utils.general_tools as GT
from utils.filepaths import Filepaths as gfiles
import utils.log_file as log
import utils.ui_utils.progress_bar as ui_progress_bar
import utils.assets_tools as AT
import sys
import re

def extract_unused_assets(assets_to_check):
    """
    Extract unused assets by comparing provided assets with those found in specified files.

    Args:
        assets_to_check (list): List of file paths to check against used assets.

    Returns:
        list: Paths of unused assets that were moved.
    """
    files_to_scan = [
        gfiles.bullets(),
        gfiles.explosions(),
        gfiles.materials3d(),
        gfiles.weapons(),
        gfiles.startmenu(),
        gfiles.game_file_path(),
    ]
    files_to_scan.extend(gfiles.levels_path())
    files_to_scan.extend(gfiles.particles_path())

    # Initialize lists
    used_assets = set()
    unused_assets = []
    extracted_assets = []

    reference_names = {
        asset: AT.get_reference_name(asset)
        for asset in assets_to_check
        if AT.get_reference_name(asset)  # Filtrer les références vides
        }
    
    # Step 1: Extract used assets from files
    for file_path in files_to_scan:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Check if any reference name exists in the line
                    for asset, ref_name in reference_names.items():
                        if ref_name in line:
                            used_assets.add(asset)
        except Exception as e:
            states.set_error_found(f"Error reading file {file_path}: {e}")
            extracted_assets.append(f"Error extracting from {file_path}")

    # Step 2: Identify unused assets
    for asset in assets_to_check:
        if asset not in used_assets:
            unused_assets.append(asset)

    # Step 3: Move unused assets to "Unused Assets" directory
    unused_assets_dir = os.path.join(states.root_path, "Unused Assets")
    for asset in unused_assets:
        new_path = asset.replace("Assets", "Unused Assets", 1)
        new_dir = os.path.dirname(new_path)

        # Create directories if they don't exist
        os.makedirs(new_dir, exist_ok=True)

        try:
            shutil.move(asset, new_path)
            log.debug(f"Moved {asset} -> {new_path}")
            extracted_assets.append(asset)
        except Exception as e:
            states.set_error_found(f"Error moving {asset} to {new_path}: {e}")
            extracted_assets.append(f"Error extracting {asset}")

    ui_progress_bar.update_progress_bar(len(files_to_scan))

    return extracted_assets
