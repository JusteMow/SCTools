import os
import utils.xml_tools as XT
from lxml import etree
import utils.asset_renamer_tools_generic as ar_gen
import utils.log_file as log
import utils.gamebox_tools as GB
import states.states as states
import utils.general_tools as GT

# Function to rename assets in levels
def rename_asset_in_levels(old_path, new_path, overwrite_screenName):
    global found_errors
    sucess = True

    try:
        log.debug("Start processing levels")
        levels_path = os.path.normpath(os.path.join(states.root_path, "levels"))
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        
        for file_name in os.listdir(levels_path):
            if not file_name.endswith(".level"):
                continue

            level_file_path = os.path.join(levels_path, file_name)
   		
            try:
                root = XT.get_root(level_file_path)

                if "Assets\\Models\\Enemies\\Sprites" in old_path:
                    root = rename_asset_in_level_waves(root, old_name, new_name, overwrite_screenName)
                if "Assets\\Models\\Players\\Sprites" in old_path:
                    root = rename_asset_in_levels_player(root, old_name, new_name, overwrite_screenName)
                if "Assets\\Pictures" in old_path:
                    root = rename_asset_in_level_pictures(root, old_name, new_name)
                if "Assets\\Models\\Items\\Sprites" in old_path:
                    root = rename_asset_in_level_item(root, old_name, new_name, overwrite_screenName)
                if "Assets\\Models\\Backgrounds\\Sprites" in old_path:
                    root = rename_asset_in_level_background(root, old_name, new_name, overwrite_screenName)

                XT.write_updated_content(level_file_path, root)

                if "Assets\\Sounds\\" in old_path:
                    rename_asset_in_level_sound(level_file_path, old_name, new_name)
            except Exception as e:
                states.set_error_found(f"Error processing file {file_name}: {e}")
                sucess = False
        log.debug("End processing levels")

    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_levels: {e}")
    return sucess



# Function to handle background sprites in levels with lxml
def rename_asset_in_level_background(root, old_name, new_name, overwrite_screenName):
    try:
        new_name_wo_extension = GB.get_name_without_extension(new_name)
        new_name_w_bg_prefix = GB.get_bg_name(new_name)

        for shmup in root.iter('shmup'):
            for bg in shmup.iter('BG'):
                if bg.get('spriteName') == old_name:
                    XT.set_property_with_log(bg, 'spriteName', new_name)

                    toybox = bg.find('toybox')
                    if toybox is not None:
                        XT.set_property_with_log(toybox, 'parentName', new_name_w_bg_prefix)
                        if overwrite_screenName:
                            XT.set_property_with_log(toybox, 'screenName', new_name_wo_extension)
                            
    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_level_background for file: {e}")
        global found_errors
        found_errors = False
    return root

# Function to handle enemy sprites in levels
def rename_asset_in_level_waves(root, old_name, new_name, overwrite_screenName):
    try:
        new_name_wo_extension = GB.get_name_without_extension(new_name)
        new_name_w_Wave_prefix = GB.get_wave_name(new_name)

        for shmup in root.iter('shmup'):
            for enemy in shmup.iter('enemy'):
                if enemy.get('spriteName') == old_name:
                    XT.set_property_with_log(enemy, 'spriteName', new_name)

                    toybox = enemy.find('toybox')
                    if toybox is not None:
                        XT.set_property_with_log(toybox, 'parentName', new_name_w_Wave_prefix)
                        if overwrite_screenName:
                            XT.set_property_with_log(toybox, 'screenName', new_name_wo_extension)

    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_level_waves for file: {e}")
        global found_errors
        found_errors = False
    return root

# Function to handle player sprites in levels	
def rename_asset_in_levels_player(root, old_name, new_name, overwrite_screenName):
    try:
        new_name_wo_extension = GB.get_name_without_extension(new_name)
        new_name_w_Player_prefix = GB.get_player_name(new_name)

        for shmup in root.iter('shmup'):
            for player in shmup.iter('player'):
                if player.get('spriteName') == old_name:
                    XT.set_property_with_log(player, 'spriteName', new_name)

                    toybox = player.find('toybox')
                    if toybox is not None:
                        XT.set_property_with_log(toybox, 'parentName', new_name_w_Player_prefix)
                        if overwrite_screenName:
                            XT.set_property_with_log(toybox, 'screenName', new_name_wo_extension)						
    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_level_item for file: {e}")
        global found_errors
        found_errors = False
    
    return root

# Function to handle pictures in levels
def rename_asset_in_level_pictures(root, old_name, new_name):
    try:
        # Utiliser XPath pour trouver tous les éléments <Background>
        backgrounds = root.findall(".//Level/Background")
        if not backgrounds:
            log.debug("No <Background> elements found.")
            return root

        # Parcourir tous les éléments <Background>
        for background in backgrounds:
            for prop_name, prop_value in background.attrib.items():
                if prop_value == old_name:
                    XT.set_property_with_log(background, prop_name, new_name)
    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_level_pictures: {e}")
        global found_errors
        found_errors = False
    return root


# Function to handle items in levels with lxml
def rename_asset_in_level_item(root, old_name, new_name, overwrite_screenName):
    try:
        new_name_wo_extension = os.path.splitext(new_name)[0]

        old_name_Item_prefix = f"Item_{os.path.splitext(os.path.basename(old_name))[0]}"
        new_name_Item_prefix = f"Item_{os.path.splitext(os.path.basename(new_name))[0]}"
        new_name_Player_prefix = ar_gen.transform_name(new_name, ar_gen.NameType.PLAYER_NAME_WO_EXT)

        for shmup in root.iter('shmup'):
            for item in shmup.iter('item'):
                if item.get('spriteName') == old_name:
                    XT.set_property_with_log(item, 'spriteName', new_name)
					
                    toybox = item.find('toybox')
                    if toybox is not None:
                        XT.set_property_with_log(toybox, 'parentName', new_name_Player_prefix)
                        if overwrite_screenName:
                            XT.set_property_with_log(toybox, 'screenName', new_name_wo_extension)		
            for enemy in shmup.iter('enemy'):   
                    item = enemy.find('ITEMS')
                    if item.get('itemSpawned') == old_name_Item_prefix:
                        XT.set_property_with_log(item, 'itemSpawned', new_name_Item_prefix)
					 
    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_level_item for file: {e}")
        global found_errors
        found_errors = False

    return root


# Function to handle sounds in levels
# this one i don't use XML, i don't remember why.
def rename_asset_in_level_sound(file_path, old_name, new_name):
    try:
        log.debug(f"Attempring to open{file_path})")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = XT.check_invalid_char(file.read())

        states.opened_gamebox = file_path

        if old_name in content:
            updated_content = content.replace(old_name, new_name)
            log_entry = f"soundname replaced in {file_path} : old : {old_name} new : new_name"
            log.log_entry(log_entry)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            log.log_entry(f"successfuly updated {file_path}")
            states.opened_gamebox=""
    except Exception as e:
        states.set_error_found(f"Error in rename_asset_in_level_sound for file {file_path}: {e}")
        global found_errors
        found_errors = False