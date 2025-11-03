import os
from lxml import etree
import utils.xml_tools as XT
import utils.gamebox_tools as GB
import states.states as states
import utils.log_file as log
import utils.general_tools as GT

def rename_asset_in_file_timeStamps(old_path, new_path):
    """
    Renames an asset reference in the files.timeStamps by replacing the old path with the new path,
    using lxml for XML parsing and logging changes.

    Args:
        old_path (str): The old asset path (relative to states.root_path) to replace.
        new_path (str): The new asset path (relative to states.root_path) to insert.

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "files.timeStamps")
    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)

        # Iterate over <FILE> elements and update meshName
        for file_element in root.iter("FILE"):
            mesh_name = file_element.get("meshName")

            if file_element.get("meshName") == os.path.normpath(old_path).replace("\\", "/"):
                
                log.debug(f"Timestamps : Found meshName: {os.path.basename(old_path)}")
                # Log the change
                # Difficulty here is that a path is root\\foler, and timestamps use root/folder
                XT.set_property_with_log(file_element, "meshName", os.path.normpath(new_path))

        # Write back the updated content
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True

    except Exception as e:
        states.set_error_found(f"Error renaming asset in files.timeStamps: {e}")
        return False

def rename_asset_in_gamebox_bullet(old_path, new_path):
    """
    Renames asset references in a bullet-type gamebox file by replacing names in specific attributes.

    Args:
        old_name (str): The old asset name to replace  (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.bullets")
    _name_ = GB.get_name_without_extension(new_name)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        
        # Read and clean content
        root = XT.get_root_in_gamebox(gamebox_path)

        # Iterate over elements and update attributes
        for element in root.iter():
            if element.get('meshName') == old_name:
                log.debug(f"Found element with meshName: {old_name}")
                XT.set_property_with_log(element, 'name', _name_)
                XT.set_property_with_log(element, 'screenName', _name_)
                XT.set_property_with_log(element, 'meshName', new_name)

        # Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox bullets: {e}")
        return False


def rename_asset_in_gamebox_background(old_path, new_path):
    """
    Renames asset references in a background-type gamebox file by replacing names in specific attributes.

    Args:
        old_name (str): The old asset name to replace (without path or extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.background")
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)
    _name_ = os.path.splitext(new_name)[0]
    _bg_name_ = GB.get_bg_name(new_path)
    _icon_name_ = GB.get_icon_name(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        # Read and clean content
        root = XT.get_root_in_gamebox(gamebox_path)

        # Iterate over elements and update attributes
        for element in root.iter():
            if element.get('spriteName') == old_name:
                log.debug(f"Found element with spriteName: {old_name}")
                XT.set_property_with_log(element, 'name', _bg_name_)
                XT.set_property_with_log(element, 'spriteName', new_name)
                # Update nested toybox element
                toybox = element.find('toybox')
                if toybox is not None:
                    XT.set_property_with_log(toybox, 'parentName', _bg_name_)
                    XT.set_property_with_log(toybox, 'screenName', _name_)
                    XT.set_property_with_log(toybox, 'thumbnail', _icon_name_)

        # Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox background: {e}")
        return False

def rename_asset_in_gamebox_explosion(old_path, new_path):
    """
    Renames asset references in an explosion-type gamebox file by replacing names in specific attributes.

    Args:
        old_name (str): The old asset name to replace (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.explosions")

    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")

        # Read and clean content
        root = XT.get_root_in_gamebox(gamebox_path)

        # Iterate over explosion elements and their sub-elements
        for explosion in root.iter('explosion'):
            for expl in explosion.findall('EXPL'):
                if expl.get('soundName') == old_name:
                    XT.set_property_with_log(expl, 'soundName', new_name)
                if expl.get('textureName') == old_name:
                    XT.set_property_with_log(expl, 'textureName', new_name)

        # Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox explosions: {e}")
        return False

def rename_asset_in_gamebox_items(old_path, new_path):
    """
    Renames asset references in an items-type gamebox file by replacing names in specific attributes.

    Args:
        old_name (str): The old asset name to replace  (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.items")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    _name_ = os.path.splitext(new_name)[0]
    _Item_name_ = GB.get_Item_name(new_name)
    _icon_name_ = GB.get_icon_name(new_name)


    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")

        # Step 1: Clean and load the XML content
		# Parser du XML avec des attributs en double. 8===========>
		# @Suny, si tu lis ça un jour, j'ai passé 3h pour faire marcher ce truc, pour virer les ForceFieldUseLife=true qui est en double dans le gb.items... 3h pour comprendre le problème, me battre avec ChatGPT, ocotogone... Finir par trouver un moyen de virer les attributs, pour utiliser les fonctions de XML... et les réinjecter après modifications. 
        cleaned_file, duplicates = XT.preprocess_and_load(gamebox_path)
        with open(cleaned_file, 'r', encoding='utf-8') as file:
            content = XT.check_invalid_char(file.read())

        # Parse content with lxml
        wrapped_content = f"<root>{content}</root>"
        parser = etree.XMLParser(remove_blank_text=False)
        root = etree.XML(wrapped_content.encode('utf-8'), parser)

        # Step 2: Modify attributes in the XML
        for item in root.iter('Item'):
            if item.get('spriteName') == old_name:
                XT.set_property_with_log(item, 'spriteName', new_name)
                XT.set_property_with_log(item, 'itemName', _Item_name_)
                toybox = item.find('toybox')
                if toybox is not None:
                    XT.set_property_with_log(toybox, 'parentName', _Item_name_)
                    XT.set_property_with_log(toybox, 'screenName', _Item_name_)
                    XT.set_property_with_log(toybox, 'thumbnail', _icon_name_)

            # Check for soundName in <SFX> sub-elements
            sfx = item.find('SFX')
            if sfx is not None and sfx.get('soundName') == old_name:
                XT.set_property_with_log(sfx, 'soundName', new_name)

        # Step 3: Write updated content and reinject duplicates
		### Réinjecter les doublons directement dans le contenu mis à jour
		### Réinjecter oui. 8==========>
		### @Suny, si tu lis aussi ça en vrai ça marche pas. Mais après j'ai lancé SC, et il plante pas. Il reconstruit le fichier l'air de rien. En plus j'ai oublié un attribut et il le modifie tout seul. Alors Ballec. Mtn rendez moi mon dimanche SVP. 						
        # updated_content = etree.tostring(root, encoding='unicode', pretty_print=True, method='xml')
        # final_content = XT.reinject_duplicates(updated_content, duplicates)

       # with open(gamebox_path, 'w', encoding='utf-8') as file:
       #     file.write(final_content)

        # Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True

    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox items: {e}")
        return False

	
def rename_asset_in_gamebox_pictures(old_path, new_path):
    """
    Renames asset references in a pictures-type gamebox file by replacing names in specific attributes.

    Args:
        old_name (str): The old asset name to replace (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """

    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.pictures")
        
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)
    _name_ = os.path.splitext(new_name)[0]

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")

        # Step 1: Clean the content
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 3: Modify attributes in Picture elements
        for picture in root.iter('Picture'):
            if picture.get('name') == old_name:
                XT.set_property_with_log(picture, 'name', new_name)
                XT.set_property_with_log(picture, 'screenName', _name_)

        # Step 4: Write back the updated content
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox pictures: {e}")
        return False

		
def rename_asset_in_gamebox_players_playerSprite( old_path, new_path):
    """
    Renames player sprite references in gamebox.players by updating specific attributes.

    Args:
        old_name (str): The old asset name to replace (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.players")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    _name_ = os.path.splitext(new_name)[0]
    _icon_name_ =  GB.get_icon_name(new_name)
    _Player_name_ = GB.get_player_name(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")

        # Step 1: Clean and parse content
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 2: Update player attributes
        for player in root.iter('player'):
            if player.get('spriteName') == old_name:
                XT.set_property_with_log(player, 'playerName', _Player_name_)
                XT.set_property_with_log(player, 'spriteName', new_name)

                toybox = player.find('toybox')
                if toybox is not None:
                    XT.set_property_with_log(toybox, 'parentName', _Player_name_)
                    XT.set_property_with_log(toybox, 'screenName', _name_)
                    XT.set_property_with_log(toybox, 'thumbnail', _icon_name_)

        # Step 3: Write back updated content
        XT.write_updated_wrapped_content(gamebox_path, root)

        log.debug(f"File updated successfully: {gamebox_path}")
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming player sprite in gamebox players: {e}")
        return False


def rename_asset_in_gamebox_players_Sounds(old_path, new_path):
    """
    Renames sound references in gamebox.players by updating specific gameplay attributes.

    Args:
        old_name (str): The old asset name to replace (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.players")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 2: Update gameplay sound attributes
        for player in root.iter('player'):
            gameplay = player.find('gameplay')
            if gameplay is not None:
                if gameplay.get('collisionSound') == old_name:
                    XT.set_property_with_log(gameplay, 'collisionSound', new_name)
                if gameplay.get('collisionBulletsSound') == old_name:
                    XT.set_property_with_log(gameplay, 'collisionBulletsSound', new_name)

        # Step 3: Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)

        return True
    except Exception as e:
        states.set_error_found(f"Error renaming player sounds in gamebox players: {e}")
        return False


def rename_asset_in_gamebox_sounds(old_path, new_path):
    """
    Renames sound references in gamebox.sounds by updating specific attributes.

    Args:
        old_name (str): The old asset name to replace (without path or extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.sounds")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 2: Update SOUND attributes
        for sound in root.iter('SOUND'):
            if sound.get('soundName') == old_name:
                XT.set_property_with_log(sound, 'soundName', new_name)
                XT.set_property_with_log(sound, 'screenName', new_name)

        # Step 3: Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)

        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox sounds: {e}")
        return False

		
def rename_asset_in_gamebox_sprites(old_path, new_path):
    """
    Renames sprite references in gamebox.sprites by updating specific attributes.

    Args:
        old_name (str): The old asset name to replace (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.sprites")

    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 2: Update Picture attributes
        for picture in root.iter('Picture'):
            if picture.get('name') == old_name:
                XT.set_property_with_log(picture, 'name', new_name)
                XT.set_property_with_log(picture, 'screenName', new_name)

        # Step 3: Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox sprites: {e}")
        return False

		
def rename_asset_in_gamebox_waves_sprites(old_path, new_path):
    """
    Renames asset references in a waves-type gamebox file for sprites by replacing names in specific attributes.

    Args:
        old_name (str): The old asset name to replace (with extension).
        new_name (str): The new asset name to insert (with extension).

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.waves")

    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 3: Iterate over enemy elements and update attributes
        for enemy in root.iter('enemy'):
            if enemy.get('spriteName') == old_name:
                GB.rename_enemy_element(enemy, new_name)
                
        # Step 4: Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)

        log.debug(f"File updated successfully: {gamebox_path}")
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming asset in gamebox waves: {e}")
        return False


def rename_asset_in_gamebox_waves_sounds(old_path, new_path):
    """
    Renames sound references in gamebox.waves by updating specific attributes.

    Args:
        old_name (str): The old asset name to replace.
        new_name (str): The new asset name to insert.

    Returns:
        bool: True if the file was successfully updated, False otherwise.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.waves")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)

        # Step 2: Iterate over enemy elements and update attributes
        for enemy in root.iter('enemy'):
            sound = enemy.find('SOUND')
            if sound is not None and sound.get('startSoundName') == old_name:
                XT.set_property_with_log(sound, 'startSoundName', new_name)

        # Step 3: Write updated content back to the file
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming sound in gamebox waves: {e}")
        return False


def rename_asset_in_gamebox_waypoints(old_path, new_path):
    """
    Renames sound references in gamebox.waypoints by updating specific attributes.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.waypoints")

    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)
        
        # Iterate over waypoint elements
        for waypoint in root.iter('waypoint'):
            behaviors = waypoint.find('behaviors')
            if behaviors is not None and behaviors.get('soundName') == old_name:
                XT.set_property_with_log(behaviors, 'soundName', new_name)
        
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming sound in gamebox waypoints: {e}")
        return False


def rename_bullet_asset_in_gamebox_weapons_sprites(old_path, new_path):
    """
    Renames sprite references in gamebox.weapons by updating specific attributes.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.weapons")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    _old_name_ = os.path.splitext(old_name)[0]
    _name_ = os.path.splitext(new_name)[0]
    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)
        
        # Iterate over weapon elements
        for weapon in root.iter('weapon'):
            apparence = weapon.find('apparence')
            if apparence is not None and apparence.get('meshName') == _old_name_:
                XT.set_property_with_log(apparence, 'meshName', _name_)
        
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming sprites in gamebox weapons: {e}")
        return False
    
def rename_particle_asset_in_gamebox_weapons(old_path, new_path):
    """
    Renames sprite references in gamebox.weapons by updating specific attributes.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.weapons")
    
    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)
        
        # Iterate over weapon elements
        for weapon in root.iter('weapon'):
            apparence = weapon.find('apparence')
            if apparence is not None and apparence.get('trailMaterial') == old_name:
                XT.set_property_with_log(apparence, 'trailMaterial', new_name)
        
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming sprites in gamebox weapons: {e}")
        return False


def rename_asset_in_gamebox_weapons_sounds(old_path, new_path):
    """
    Renames sound references in gamebox.weapons by updating specific attributes.
    """
    gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.weapons")

    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)

    try:
        log.debug(f"Attempting to parse XML file: {gamebox_path}")
        root = XT.get_root_in_gamebox(gamebox_path)
        
        # Iterate over weapon elements
        for weapon in root.iter('weapon'):
            sound = weapon.find('Sound')
            if sound is not None:
                if sound.get('shot') == old_name:
                    XT.set_property_with_log(sound, 'shot', new_name)
                if sound.get('impactSoundName') == old_name:
                    XT.set_property_with_log(sound, 'impactSoundName', new_name)
                if sound.get('chargeSoundName') == old_name:
                    XT.set_property_with_log(sound, 'chargeSoundName', new_name)
                if sound.get('chargeSoundReadyName') == old_name:
                    XT.set_property_with_log(sound, 'chargeSoundReadyName', new_name)
        
        XT.write_updated_wrapped_content(gamebox_path, root)
        return True
    except Exception as e:
        states.set_error_found(f"Error renaming sounds in gamebox weapons: {e}")
        return False
		

def replace_in_particle_cache_files(old_path, new_path):
    """
    Replaces all occurrences of `old_name` with `new_name` in particle cache files, 
    excluding files with '_back' in their names, and logs the changes.

    Args:
        old_name (str): The string to replace.
        new_name (str): The replacement string.

    Returns:
        bool: True if all files are processed successfully, False otherwise.
    """
    cache_folder = os.path.join(states.root_path, "gamebox", "Cache", "Particles")

    old_name = os.path.basename(old_path)
    new_name = os.path.basename(new_path)
    

    try:
        log.debug(f"Searching in Cache\\Particles\\")

        # List all files in the folder
        for file_name in os.listdir(cache_folder):
            if '_back' in file_name:
                continue  # Skip files with '_back' in their names

            file_path = os.path.join(cache_folder, file_name)

            # Ensure we process only files
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = XT.check_invalid_char(file.read())
                
                if old_name in content:
                    #replace by name
                    updated_content = content.replace(old_name, new_name)
                
                    # Write changes if replacements occurred
                    log.log_stuff(f"updated line 6 in Material in {file_path}", old_name, new_name)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)

        log.debug("All applicable files processed successfully.")
        return True
    except Exception as e:
        states.set_error_found(f"Error processing particle cache files: {e}")
        return False


