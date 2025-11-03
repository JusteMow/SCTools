import os
import states.states as states
import utils.clone_tools as clone_tools
import utils.xml_tools as XT
from tkinter import messagebox
from tkshared.general import ScreenNameFilter
import utils.gamebox_tools as GB
from lxml import etree
import utils.log_file as log
import utils.general_tools as GT


def rename_level_filename(selected_level, destination_level):
    """
    rename level file to another level, and adapt all others levels and references
    Args: 
        levels (str) must be formated level000 without path
    """
    selected_level_ = os.path.splitext(selected_level)[0]
    destination_level_ = os.path.splitext(destination_level)[0]

    log.log_entry(f"Start renaming  {selected_level_} to {destination_level_}...")
    adjust_level_references(selected_level_, destination_level_)
    update_game_file_levels(selected_level_, destination_level_)
    rename_level_files(selected_level_, destination_level_)
    rename_thumbnails_files(selected_level_, destination_level_)
    log.log_entry(f"End rename {selected_level_} to {destination_level_} : Success !")

def clone_and_insert_level(original_level_number, clone_level_number, clone_screen_name):
    """
    clones the level file, insert it after the cloned one, clones the thumbnail, and sets the new screen name
    Args: 
        original_level_number and clone_level_number (str) as Level000  without extension 
    """
    
    log.log_entry(f"Start cloning  {original_level_number} to {clone_level_number}...")

    temp_clone_number = get_last_level_plus_one()
    
    #Step1 clone the level file with the temp name
    path_original_level = get_level_filename(original_level_number)
    clone_tools.clone_file(path_original_level, f"{temp_clone_number}.level")

    #Step2 clone the thumbnail file with the temp name
    path_original_thumbnail = get_level_thumbnail_filename(original_level_number)
    if os.path.exists(path_original_thumbnail):
        temp_thumbnail_filename = (os.path.basename(path_original_thumbnail)).replace(original_level_number, temp_clone_number)
        clone_tools.clone_file(path_original_thumbnail, temp_thumbnail_filename)

    #step3 modify the gamebox and .game file
    set_level_screenName(get_level_filename(temp_clone_number), clone_screen_name)
    add_cloned_level_to_gamefile(original_level_number, temp_clone_number, clone_screen_name)

    #Step4 set it at its place.
    rename_level_filename(os.path.splitext(temp_clone_number)[0], clone_level_number)

    log.log_entry(f"End cloning  {original_level_number} to {clone_level_number} : Success !")

def set_level_screenName(level_file, screen_name):
    if not os.path.exists(level_file): 
        states.set_error_found (f"Error : level file doesn't exist : {level_file}")
        return
    
    root = XT.get_root(level_file)
    level = root.find(".//Level")
    XT.set_property_with_log(level, "screenName", screen_name )
    XT.write_updated_content(level_file,  root)

def add_cloned_level_to_gamefile(original_number, clone_level_number, clone_level_screen_name):
    """
    Adds a cloned level to the .game file.

    Args:
        original_number (str): The name of the original level to clone (e.g., 'level001').
        clone_level_number (str): The number for the cloned level (e.g., 'level002').
        clone_level_name (str): The screenName for the cloned level.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        # Parse the .game file
        game_file = GT.get_game_file()

        root = XT.get_root(game_file)

        # Find the original level
        original_level = ""
        for level in root.findall(".//LEVEL"):
            if level.get("name") == original_number:
                original_level = level
                break

        if original_level == "":
            states.set_error_found(f"Error: Original level '{original_number}' not found in the .game file.")
            return False

        # Clone the level
        cloned_level = etree.Element("LEVEL")
        for attrib, value in original_level.attrib.items():
            cloned_level.set(attrib, value)
        
        # Update the cloned level's attributes
        XT.set_property_with_log(cloned_level, "name", clone_level_number)
        XT.set_property_with_log(cloned_level, "screenName", clone_level_screen_name)

        original_level.addnext(cloned_level)
    
        # Write the updated .game file back to disk
        XT.write_updated_content(game_file, root)
        log.log_entry(f"Cloned level '{clone_level_number}' successfully added to the .game file.")
        return True

    except Exception as e:
        states.set_error_found(f"Error adding cloned level: {e}")
        return False

def get_last_level_plus_one():
    """
    Retrieves the next available level number based on the existing levels in the directory.

    Returns:
        str : level xxx .level 
    """
    levels_path = os.path.join(states.root_path, "levels")
    if not os.path.exists(levels_path):
        raise FileNotFoundError(f"Levels directory not found: {levels_path}")

    max_level_number = 0

    for file in os.listdir(levels_path):
        if file.endswith(".level") and file.startswith("level"):
            try:
                # Extract the numeric part of the level name
                level_number = int(file[5:8])
                max_level_number = max(max_level_number, level_number)
            except ValueError:
                # Skip files that don't conform to the expected naming convention
                continue
    
    virtual_max_level = f"level{(max_level_number + 1):03d}"

    return virtual_max_level


def get_level_filename(level_xxx, add_extension=True):
    """
    Returns the full path of a level file.
    Args:
        level_xxx (str): Level identifier (e.g., 'level001').
        add_extension (bool): Whether to add the '.level' extension.
    Returns:
        str: Full path of the level file.
    """
    file_name = f"{level_xxx}.level" if add_extension else level_xxx
    return os.path.join(states.root_path, "levels", file_name)


def rename_level_files(level_aaa, level_bbb):
    """
    Renames level files to adjust their numbering, shifting all files between level_aaa and level_bbb inclusively.

    Args:
        level_aaa (str): The initial level name (e.g., "level003").
        level_bbb (str): The target level name (e.g., "level005").

    Returns:
        None
    """
    log.log_entry(f"Start renaming levels  {level_aaa} to {level_bbb}...")
    
    path_level_aaa = get_level_filename(level_aaa)

    # Step 1: Temporarily rename the source file
    if not os.path.exists(path_level_aaa):
        states.set_error_found(f"Error: {path_level_aaa} does not exist.")
        return

    #temporaire pour ne pas confondre avec celui qui a déjà ce nom, puisqu'on insère à terme. 
    path_level_aaa_temp = f"{path_level_aaa}.TempFileShouldNotAppear"

    os.rename(path_level_aaa, path_level_aaa_temp)
    log.debug(f"Temporarily renamed {path_level_aaa} -> {path_level_aaa_temp}")

    # Determine iteration direction
    direction = 1 if int(level_bbb[5:]) > int(level_aaa[5:]) else -1

    # Step 2: Replace LevelXXX -> LevelXXX ± 1
    current = int(level_aaa[5:]) + direction
    target = int(level_bbb[5:])

    while current != target + direction:
        current_level = f"level{current:03d}"
        next_level = f"level{current - direction:03d}"

        path_current = get_level_filename(current_level)
        path_next = get_level_filename(next_level)

        if os.path.exists(path_current):
            os.rename(path_current, path_next)
            log.log_rename_file(path_current, path_next)

        current += direction

    # Step 3: Rename the temporary file to the target name
    path_level_bbb = get_level_filename(level_bbb)
    os.rename(path_level_aaa_temp, path_level_bbb)
    log.log_rename_file(path_level_aaa_temp, path_level_bbb)
    log.log_entry(f"End renaming levels  {level_aaa} to {level_bbb} : Success ! ")

import os

def get_level_thumbnail_filename(level_name):
    """
    Returns the full path of a level's thumbnail file.
    
    Args:
        level_name (str): Level identifier (e.g., 'level001').
    
    Returns:
        str: Full path of the thumbnail file, or None if not found.
    """
    filename = f"{GT.get_project_name()}_{level_name}_thumb.png"
    thumbnail_path = os.path.join(states.root_path, "levels", "_thumbnails", filename)
    
    # Look for the thumbnail file that contains the level name
    return thumbnail_path
    


def rename_thumbnails_files(level_aaa, level_bbb):
    """
    Renames thumbnail files to adjust their numbering, shifting all files between level_aaa and level_bbb inclusively.

    Args:
        level_aaa (str): The initial level name (e.g., "level003").
        level_bbb (str): The target level name (e.g., "level005").

    Returns:
        None
    """
    
    log.log_entry(f"Start renaming levels thumbnails  {level_aaa} to {level_bbb}... ")

    path_level_thumbnail_aaa = get_level_thumbnail_filename(level_aaa)
    if not path_level_thumbnail_aaa:
        print(f"Error: Thumbnail for {level_aaa} not found.")
        return

    path_level_thumbnail_temp = f"{path_level_thumbnail_aaa}.TempFileShouldNotAppear"

    # Step 1: Temporarily rename the source file
    # For some reason, i don't always have a thumbnail file
    if os.path.exists(path_level_thumbnail_aaa):
        os.rename(path_level_thumbnail_aaa, path_level_thumbnail_temp)
        log.log_rename_file(f"(temporary->){path_level_thumbnail_aaa}", path_level_thumbnail_temp )

    # Determine iteration direction
    direction = 1 if int(level_bbb[5:]) > int(level_aaa[5:]) else -1

    # Step 2: Replace LevelXXX -> LevelXXX ± 1
    current = int(level_aaa[5:]) + direction
    target = int(level_bbb[5:])

    while current != target + direction:
        current_level = f"level{current:03d}"
        next_level = f"level{current - direction:03d}"

        path_current = get_level_thumbnail_filename(current_level)
        path_next = get_level_thumbnail_filename(next_level)

        if path_current and os.path.exists(path_current):
            os.rename(path_current, path_next)
            log.log_rename_file(path_current, path_next)

        current += direction

    # Step 3: Rename the temporary file to the target name
    path_level_thumbnail_bbb = get_level_thumbnail_filename(level_bbb)
    os.rename(path_level_thumbnail_temp, path_level_thumbnail_bbb)
    log.log_rename_file(path_level_thumbnail_temp, path_level_thumbnail_bbb)
    log.log_entry(f"End renaming levels thumbnails  {level_aaa} to {level_bbb} : Success! ")



def update_game_file_levels(level_aaa, level_bbb):
    """
    Updates the LEVEL.name attributes in the .game file to adjust numbering,
    shifting all levels between level_aaa and level_bbb inclusively.

    Args:
        level_aaa (str): The initial level name (e.g., "level003").
        level_bbb (str): The target level name (e.g., "level005").

    Returns:
        None
    """
    log.log_entry(f"Start updating game file levels {level_aaa} to {level_bbb}... ")
    # Localiser le fichier .game
    game_file_path = GT.get_game_file()

    try:
        # Parse the .game file
        root = XT.get_root(game_file_path)

        # Trouver tous les niveaux dans root.LEVEL
        levels = [level for level in root.findall(".//LEVEL")]

        # Étape 1 : Renommer level_aaa -> level_aaa_TempShouldNotAppear
        for level in levels:
            if level.get("name") == level_aaa:
                XT.set_property_with_log(level, "name", f"{level_aaa}_TempShouldNotAppear" )
                break

        # Déterminer la direction
        direction = 1 if int(level_bbb[5:]) > int(level_aaa[5:]) else -1

        # Étape 2 : Décaler les niveaux
        current = int(level_aaa[5:]) + direction
        target = int(level_bbb[5:])
        while current != target + direction:
            current_level = f"level{current:03d}"
            next_level = f"level{current - direction:03d}"

            for level in levels:
                if level.get("name") == current_level:
                    XT.set_property_with_log(level, "name", next_level )
                    break

            current += direction

        # Étape 3 : Renommer level_aaa_TempShouldNotAppear -> level_bbb
        for level in levels:
            
            if level.get("name") == f"{level_aaa}_TempShouldNotAppear":
                XT.set_property_with_log(level, "name", level_bbb )
                break

        # Sauvegarder les modifications dans le fichier
        XT.write_updated_content(game_file_path, root)
        log.log_entry(f"End updating game file levels {level_aaa} to {level_bbb} : Success!  ")
    except Exception as e:
        states.set_error_found(f"Error updating .game file: {e}")


def adjust_level_references(level_aaa, level_bbb):
    """
    Adjusts level references across all .level files based on the desired renaming order.

    Args:
        level_aaa (str): Original level name (e.g., "level003").
        level_bbb (str): Destination level name (e.g., "level005").
    """

    log.log_entry(f"Start updating level reference in levels {level_aaa} to {level_bbb}...  ")

    levels_path = os.path.join(states.root_path, "levels")
    temp_value = f"{level_aaa}-TempValueShouldNotAppear"

    # Step 1: Replace all references to LevelAAA with TempValue
    files = [os.path.join(levels_path, f) for f in os.listdir(levels_path) if f.endswith(".level")]

    for file in files:
        root = XT.get_root(file)
        updated = False
        for trigger in root.findall(".//triggers/endOfLevel"):
            next_level = trigger.get("nextLevelName")
            if next_level == level_aaa:
                XT.set_property_with_log(trigger, "nextLevelName", temp_value)
                updated = True

        if updated:
            XT.write_updated_content(file, root)

    # Determine iteration direction
    direction = 1 if int(level_bbb[5:]) > int(level_aaa[5:]) else -1

    # Step 2: Replace LevelXXX -> LevelXXX ± 1
    current = int(level_aaa[5:]) + direction
    target = int(level_bbb[5:])

    while current != target + direction:
        current_level = f"level{current:03d}"
        next_level = f"level{current - direction:03d}"
        for file in files:
            root = XT.get_root(file)
            updated = False
            for trigger in root.findall(".//triggers/endOfLevel"):
                next_level_name = trigger.get("nextLevelName")
                if next_level_name == current_level:
                    XT.set_property_with_log(trigger, "nextLevelName", next_level)
                    updated = True

            if updated:
                XT.write_updated_content(file, root)

        current += direction

    # Step 3: Replace TempValue -> LevelBBB
    for file in files:
        root = XT.get_root(file)
        updated = False
        for trigger in root.findall(".//triggers/endOfLevel"):
            next_level = trigger.get("nextLevelName")
            if next_level == temp_value:
                XT.set_property_with_log(trigger, "nextLevelName", level_bbb)
                updated = True

        if updated:
            XT.write_updated_content(file, root)

    log.log_entry(f"End updating level reference in levels {level_aaa} to {level_bbb} : sucess !  ")


def rename_level_file(old_name, new_name):
    """
    Renames a level file from old_name to new_name in the specified root path.

    Args:
        old_name (str): The current name of the level (e.g., "level001").
        new_name (str): The desired new name of the level (e.g., "level002").

    Returns:
        bool: True if the renaming was successful, False otherwise.
    """

    old_file = os.path.join(states.root_path, f"{old_name}.level")
    new_file = os.path.join(states.root_path, f"{new_name}.level")

    if not os.path.exists(old_file):
        print(f"Error: File '{old_file}' does not exist.")
        return False

    if os.path.exists(new_file):
        print(f"Error: File '{new_file}' already exists.")
        return False

    try:
        os.rename(old_file, new_file)
        log.log_rename_file(old_file, new_file)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming file: {e}")
        return False



def swap_enemies_in_levels(levels, enemy_A, enemy_B, screen_name_filter : ScreenNameFilter, overwrite_screenName: bool):
    """
    Swaps enemy A with enemy B in selected levels.

        Args : 
            levels (strà : formatted as [level001.level, level004.level]...
            enemies (str) : sprite names.png
            screen_name_filter : filter with screenName, use specific class, or set to None
            overwtrite_screenName : if true, will also swap Screen Name (displayed in Editor)
    """

    # Normalize levels to a list
    if isinstance(levels, str):
        levels = [levels]

    log.log_entry(f"Start swap enemies in level {levels} : {enemy_A} to {enemy_B} with filters ...  ")

    levels_path = os.path.join(states.root_path, "levels")

    total_updates = 0

    enemySwapWith_parentName = GB.get_wave_name(enemy_B)

    try:
        for level_file in levels:
            level_path = os.path.join(levels_path, level_file)

            if not os.path.exists(level_path):
                print(f"Error : Level file not found: {level_path}")
                continue

            # Parse the XML file
            root = XT.get_root(level_path)
            enemies_updated = 0

            # Swap enemies
            for enemy in root.iter('enemy'):
                if enemy.get("spriteName") == enemy_A:
                    screen_name = enemy.find("toybox").get("screenName")  # Récupérer le screenName
                    if screen_name_filter != None and not screen_name_filter.match_filter(screen_name):
                        continue

                    XT.set_property_with_log(enemy, 'spriteName', enemy_B)
                    toybox = enemy.find("toybox")
                    XT.set_property_with_log(toybox, 'parentName', enemySwapWith_parentName)
                    if overwrite_screenName:
                        XT.set_property_with_log(toybox, 'screenName', os.path.splitext(enemy_B)[0])
                    enemies_updated += 1
                    total_updates += 1 

            if enemies_updated > 0:
                # Write updated content back to the file
                XT.write_updated_content(level_path, root) #level PATH not lvl File.... PATH 
                log.log_entry(f"successfuly updated {enemies_updated} reference in  {level_file}")
        log.log_entry(f"End swap enemies in level {levels} : {enemy_A} to {enemy_B} with filters : Success  ")

        if total_updates > 0:
            log.debug( f"Enemies swapped successfully! {total_updates} updates made.")
        else:
            states.set_error_found("No matching enemies found to swap in selected levels.")


    except Exception as e:
        states.set_error_found(f"Failed to swap enemies in levels: {e}")