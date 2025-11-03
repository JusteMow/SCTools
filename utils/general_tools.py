import os
import states.states as states
from tkinter import messagebox
from lxml import etree
import utils.log_file as log
# NoticeLabel is now in states.notice_label

def get_all_assets():
    """
    returns all assets relative path
    """
    assets = []
    if not states.root_path:
        return

    assets_dir = os.path.join(states.root_path, "Assets")
    if not os.path.exists(assets_dir):
        messagebox.showerror("Error", "The 'Assets' folder does not exist in the selected root directory.")
        return

    for root, _, files in os.walk(assets_dir):
        for file in files:
            assets.append(os.path.join(root, file))  # Ajoute le chemin complet


    return assets

def validate_new_filename(filename, conflict_names=None, showMessage=False):
    
    if conflict_names==None:
        conflict_names = detect_all_asset_name_conflict()

    if not filename:
        if showMessage:
            messagebox.showerror(f"{filename} is empty", f"{filename} is empty")
        return False
    
    if " " in filename:
        if showMessage:
            messagebox.showerror(f"{filename} contains spaces", "{filename} contains spaces")
        return False
    
    if not validate_extension(filename):
        if showMessage:
            messagebox.showerror(f"{filename} extension not valid", f"extension can be {valid_extensions}")
        return False

    if check_new_file_conflict_with_existing_file(filename, conflict_names):
        if showMessage:
            messagebox(f"another {os.path.splitext(os.path.basename(filename))[0]} already exists. Check other folders and names with other extensions (which also conflicts sometimes)")
        return False
    
    return True

valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".psd", ".pic", ".gif", ".tga", "ppm", ".pgm", ".hdr", ".dds", ".wav", ".mp3"}

def validate_extension(file_name):
    """
    Validate if the file has an allowed extension.
    
    Args:
        file_name (str): The name of the file to validate.
    
    Returns:
        bool: True if the extension is valid, False otherwise.
    """
    
    extension = os.path.splitext(file_name)[1].lower()  # Extract and normalize extension to lowercase
    return extension in valid_extensions


def validate_new_filename_or_get_another(filepath, conflict_names=None):
    """
    Validates a filename and proposes a new one if necessary.
    Can handle file name or file path as input, and will output file name or file path.
    Will work on basename, Won't make any change nor validation to filepath.
    
    Args:
        filepath (str): The original filename/filepath to validate.
        conflict_names (set or list): A collection of existing filenames to check for conflicts. not needed, but can be specified to optimize mass operations

    Returns:
        str: A validated and conflict-free filename/filepath.
    """
    if conflict_names is None:
        conflict_names = detect_all_asset_name_conflict()

    # Handle empty filename
    if not filepath:
        messagebox.showinfo("Invalid Filename", "The provided filename is empty. Defaulting to 'aaa.aaa'.")
        return "aaa.aaa"

    # Replace spaces with underscores
    filepath = normalize_filename(filepath)

    # Check for conflicts and propose a new name if needed
    base_name, ext = os.path.splitext(filepath)  # Split filename into base name and extension
    suffix = 0  # Start suffix for alternative names

    new_base_name = f"{base_name}{ext}"
    while check_new_file_conflict_with_existing_file(new_base_name, conflict_names):
        new_base_name = f"{base_name}_{suffix:03d}{ext}"  # Append a suffix with zero padding
        suffix += 1

    return os.path.join(os.path.dirname(filepath), new_base_name)

import os

def normalize_filename(filepath):
    """
    Replace spaces in the filename with underscores while keeping the directory structure intact.
    
    Args:
        filepath (str): Full path to the file.
    
    Returns:
        str: Updated file path with spaces in the filename replaced by underscores.
    """
    dir_path, filename = os.path.split(filepath)  # Split directory and file name
    filename = filename.replace(" ", "_")         # Replace spaces in the file name
    return os.path.join(dir_path, filename)       # Rejoin directory and updated file name

def check_new_file_conflict_with_existing_file(filepath, conflict_names=None):
    """
        Use to validate that a new name won't have name conflict with already existing files
        returns True if conflict False of ,pt
        Args : 
            filepath (str) : file path or file name. 

        Returns: 
            true if conflict detected, false if  not
        
    """
    if conflict_names == None:
        conflict_names = detect_all_asset_name_conflict()

    base_name = os.path.splitext(os.path.basename(filepath))[0]
    return conflict_names.get(base_name , 0) > 0


def detect_all_asset_name_conflict(assets=None):
    """
    returns a dictionnary of all assets with same filename in different folder, even with different extensions
    if a filename as os.path.splitext(os.path.basename(filename))[0] filename key has a value >1 then it's a conflict
    if testing a new filename, if the new os.path.splitext(os.path.basename(filename))[0] has a value, then it's a conflict
    """
    if assets is None:
        assets = get_all_assets()

    name_counts = {} # dictionary too

    # will detect cross folder name conflicts, or same name with different extension conflicts. 
    # if basename without extension appears more than one time, it will be tagged as a conflict file
    for asset in assets:
        base_name = os.path.splitext(os.path.basename(asset))[0]
        name_counts[base_name] = name_counts.get(base_name, 0) + 1

    return name_counts



#====================================== game.game =--------->
def get_game_file():
    """
    Locate the .game file in the root_path directory.
    """
    # Locate the .game file
    game_file = None
    for file in os.listdir(states.root_path):
        if file.endswith(".game"):
            game_file = os.path.join(states.root_path, file)
            break  # Exit the loop once the .game file is found

    if not game_file:
        states.set_error_found("Error: .game file not found.")
        return None

    return game_file

def get_project_name():
    """
    Retrieves the project name from the .game file in the root_path.

    Args:
        root_path (str): The root directory where the .game file is located.

    Returns:
        str: The project name if found, or None if not found.
    """
    # Locate the .game file
    game_file = get_game_file()

    try:
        # Parse the .game file
        tree = etree.parse(game_file)
        root = tree.getroot()

        # Extract the project name from the GAME element's "name" attribute
        project_name = root.find(".//GAME").get("name")

        return project_name
    except Exception as e:
        states.set_error_found(f"Error parsing .game file: {e}")
        return None

# ============================== Files manipulation ==========---> 
def rename_file(old_file_path, new_file_path):
    """
    Renames a file on the disk while ensuring it is writable and accessible.

    Args:
        old_file_path (str): The current path of the file.
        new_file_path (str): The desired new path for the file.

    Returns:
        bool: True if the file was successfully renamed, False otherwise.
    """

    success=False
    try:
  
        # Vérification si le fichier source existe
        # here, case sensitiveness throw erros with icons files
        if not os.path.exists(old_file_path):
            states.set_error_found(f"Error: File not found: {old_file_path}")
            return False

        # Vérification si le fichier destination existe déjà
        # here we have to be case sensitive because AAA.png may be renamed aaa.png 
        # but don't throw an error if file already exists, it can happen with icons. 
        if path_exists_case_sensitive(new_file_path):
            states.set_warning_found(f"Warning : Target file already exists: {new_file_path}")
            return False

        # Vérification de l'accès en lecture et écriture
        if not os.access(old_file_path, os.R_OK | os.W_OK):
            states.set_error_found(f"Error: File is not accessible or writable: {old_file_path}")
            return False

        # Tentative de renommage
        os.rename(old_file_path, new_file_path)
        log.log_rename_file(old_file_path, new_file_path)
        success=True
    except Exception as e:
        states.set_error_found(f"Error renaming file: {e}")

    return success


import re

import os
import re

def convert_to_snake_case(filename):
    """
    Convert a filename to snake_case while preserving specific suffixes.
    
    Args:
        filename (str): The input filename to convert.
    
    Returns:
        str: The filename in snake_case format.
    """
    # Define the suffixes to preserve
    suffixes_to_preserve = ["_TURRET", "_CANON", "_BODY", "_TAIL"]
    
    # Separate the base name and extension
    name, ext = os.path.splitext(filename)
    
    # Check if the name ends with any of the special suffixes
    preserved_suffix = ""
    for suffix in suffixes_to_preserve:
        if name.endswith(suffix):
            preserved_suffix = suffix
            name = name[: -len(suffix)]  # Remove the suffix from the name for processing
            break
    
    # Replace delimiters (-, ., etc.) with underscores
    name = re.sub(r'[.\-]+', '_', name)
    
    # Handle uppercase letters, avoiding double underscores
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)  # Handle cases like ABCDef -> ABC_Def
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)      # Handle cases like abcDef -> abc_Def
    
    # Convert all to lowercase while preserving underscores
    name = name.lower()
    
    # Re-add the preserved suffix and extension
    return f"{name}{preserved_suffix}{ext}"


def path_exists_case_sensitive(file_path):
    """
    Vérifie si un fichier existe, en tenant compte de la casse.
    """
    directory, file_name = os.path.split(file_path)
    if not os.path.exists(directory):  # Vérifie si le répertoire existe
        return False

    return file_name in os.listdir(directory)


#======================= Process notification =================== >
def start_process(name): 
    states.reset_errors()
    states.end_process_log=[]
    log.log_entry(f"start process :  {name}", True)
    states.progress_bar=0
    if states.notice_label:
        states.notice_label.set_text(f"Processing : {name}")

def end_process(name, log_entry=None, show_dialog=False):
    errors, warnings = states.get_errors()
    if states.notice_label:
        states.notice_label.set_text(f"Ready !")
    display_log_entry = (
        f"All ok ! \n {states.end_process_log}"
        if log_entry is None
        else f"Errors detected: see log in details, in project root_folder, search sctool.log, open with notepad, and ctrl+f 'Error'\n{log_entry}"
        if errors
        else f"Warning detected: most of the time, should be good, but see log in details, in project root folder, search sctool.log, open with notepad, and ctrl+f 'Warning'\n{log_entry}"
        if warnings
        else f"All Ok\n{log_entry}"
    )
    log.log_entry(display_log_entry, True)
    if errors:
        messagebox.showerror(name, display_log_entry )
    elif warnings:
        messagebox.showwarning(name, display_log_entry )
    else:
        messagebox.showinfo(name, display_log_entry)


