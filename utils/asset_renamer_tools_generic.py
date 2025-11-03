import os
from lxml import etree
from enum import Enum
from enum import Enum
import utils.xml_tools as XT
import utils.log_file as log
import states.states as states
import utils.general_tools as GT

class NameType(Enum):
    NAME = "name"
    NAME_WO_EXT = "name_wo_ext"
    BG_NAME_WO_EXT = "bg_name_wo_ext"
    ITEM_NAME_WO_EXT = "Item_name_wo_ext"
    ICON_NAME_WO_EXT = "icon_name_wo_ext"
    ICONW_NAME_WO_EXT = "iconW_name_wo_ext"
    WAVE_NAME_WO_EXT = "Wave_name_wo_ext"
    PLAYER_NAME_WO_EXT = "Player"

    # Helper to transform names
def transform_name(name, name_type):
    """
    Transforms a given name based on its NameType.

    Args:
        name (str): The original name.
        name_type (NameType): The type of transformation to apply.

    Returns:
        str: The transformed name.
    """
    if name_type == NameType.NAME:
        return name
    elif name_type == NameType.NAME_WO_EXT:
        return os.path.splitext(os.path.basename(name))[0]
    elif name_type == NameType.BG_NAME_WO_EXT:
        return f"bg_{os.path.splitext(os.path.basename(name))[0]}"
    elif name_type == NameType.ITEM_NAME_WO_EXT:
        return f"Item_{os.path.splitext(os.path.basename(name))[0]}"
    elif name_type == NameType.ICON_NAME_WO_EXT:
        return f"icon_{os.path.splitext(os.path.basename(name))[0]}"
    elif name_type == NameType.ICONW_NAME_WO_EXT:
        return f"iconW_{os.path.splitext(os.path.basename(name))[0]}"
    elif name_type == NameType.WAVE_NAME_WO_EXT:
        return f"Wave_{os.path.splitext(os.path.basename(name))[0]}"
    elif name_type == NameType.PLAYER_NAME_WO_EXT:
        return f"Player_{os.path.splitext(os.path.basename(name))[0]}"
    else:
        raise ValueError(f"Unknown NameType: {name_type}")

def convert_to_sections(input_paths):
    """
    Converts a list of input paths and name types into a formatted sections_to_update list.

    Args:
        input_paths (list): A list of tuples in the form ("input_path", "name_type").

    Returns:
        list: A formatted sections_to_update list.
    """
    sections_to_update = []

    for input_path, name_type in input_paths:
        # Split the input path into its components
        parts = input_path.split(".")
        if len(parts) < 2:
            raise ValueError(f"Invalid input_path format: {input_path}")

        # Extract section, attribute, and optional path
        section = parts[0]
        attribute = parts[-1]
        path = "/".join(parts[1:-1]) if len(parts) > 2 else None

        # Append the formatted entry to the list
        sections_to_update.append((section, path, [attribute], name_type))

    return sections_to_update


def rename_asset_in_gamebox_generic(target_file_path, input_paths, old_file_path, new_file_path):
    """
    Generic function to rename asset references in an XML file by updating specific attributes,
    handling different levels of nesting.

    Args:
        file_path (str): The path of the XML file to process.
        old_name (str): The old asset name to replace.
        new_name (str): The new asset name to insert.
        sections_to_update (list): List of sections with attributes and navigation logic.

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    
    root_path = states.root_path


    target_full_path = os.path.join(root_path, target_file_path)
    old_name = os.path.basename(old_file_path)
    new_name =	os.path.basename(new_file_path)

    sections_to_update = convert_to_sections(input_paths)

    try:
        log.debug(f"Attempting to parse XML file: {target_full_path}")
        with open(target_full_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the content
        root = XT.get_root(target_full_path)

        # Iterate through sections and update attributes
        for section in sections_to_update:
            tag = section[0]  # First element of the tuple is the tag
            path = section[1]  # Second element is the path (or None)
            attributes = section[2]  # Third element is the list is the attribute
            name_type = section[3]
            transformed_old_name = transform_name(old_name, name_type)
            transformed_new_name = transform_name(new_name, name_type)

            for element in root.iter(tag):
                # Navigate if path is specified
                target_element = element.find(path) if path else element
                if target_element is None:
                    continue

                for attr in attributes:
                    if target_element.get(attr) == transformed_old_name:
                        log.debug(f"Found {attr} in <{tag}>: {transformed_old_name}")
                        XT.set_property_with_log(target_element, attr, transformed_new_name)

        # Write back the updated content
        XT.write_updated_content(target_full_path, root)
        return True

    except Exception as e:
        states.set_error_found(f"Error processing file {target_file_path}: {e}")
        return False
