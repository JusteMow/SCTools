import os
from tkinter import messagebox
import states.states as states
import utils.log_file as log
import shutil
import old.old_filename_rules as old_filename_rules
import utils.xml_tools as XT
import utils.gamebox_tools as GB
import  utils.general_tools as GT


def clone_file(original_file, clone_name, ignore_already_exist=False): 
    """
    will validate filename and  copy the file in same folder.
    Args: 
        original_file: must contain the file_path
        file will be cloned in same path
    """
    # Récupérer l'ennemi sélectionné

    if not original_file:
        messagebox.showerror("Error", "Please select an enemy to clone.")
        return False

    new_name = GT.validate_new_filename_or_get_another(os.path.basename(clone_name))

    # Fichier source et destination
    dest_file = os.path.join(os.path.dirname(original_file), new_name)

    if os.path.exists(dest_file):
        if (ignore_already_exist):
            log.debug (f"{dest_file}already exists. no new clone created")
        else: 
            states.set_error_found( f"The file '{new_name}' already exists.")
        return False
    
    try:
        # Étape 1 : Copier le fichier asset 
        shutil.copyfile(original_file, dest_file)

        log.log_clone(original_file, dest_file)
        return True
    
    except Exception as e:
        states.set_error_found(f"Failed to clone file: {e}")
        return False
    

def clone_enemy(original_path, clone_name, ignore_already_exist=False):
    """
        clones enemy file and enemy entry in gameox.waves
            Args: 
                original_path : fullpath to the sprite.extension
                clone_name (str) : just the clone_name, without path, without extnesion

    """
    if not clone_file(original_path, clone_name):
        return
    
    original_name = os.path.basename(original_path)

    try:
        # Étape 2 : Parser gamebox.waves
        gamebox_path = os.path.join(states.root_path, "gamebox", "gamebox.waves")
        root = XT.get_root_in_gamebox(gamebox_path)

        for enemy in root.iter("enemy"):
            if enemy.get("spriteName") == original_name:
                # Cloner l'ennemi
                new_enemy = XT.clone_element(enemy)
                new_enemy = GB.rename_enemy_element(new_enemy, clone_name)

                # Insérer après l'ennemi courant
                parent = enemy.getparent()
                if parent is not None:
                    index = parent.index(enemy)
                    parent.insert(index + 1, new_enemy)
                    log.log_entry(f"Added {clone_name} to gamebox.waves")

                else:
                    raise ValueError("The enemy element has no parent.")
                break

        # Étape 4 : Enregistrer les modifications
        XT.write_updated_wrapped_content(gamebox_path, root)

    except Exception as e:
        states.set_error_found(f"Failed to clone enemy: {e}")