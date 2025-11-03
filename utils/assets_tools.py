import os

def is_background_sprite(file_path): 
    return "Assets\\Models\\Backgrounds\\Sprites" in file_path

def is_bullet(file_path):
    return "Assets\\Models\\Bullets" in file_path

def is_sound(file_path):
    return "Assets\\Sounds\\SoundFX" in file_path

def is_music(file_path): 
    return "Assets\\Sounds\\Music" in file_path

def is_picture(file_path):
    return "Assets\\Pictures" in file_path

def is_enemy_sprite(file_path):
    return "Assets\\Models\\Enemies\\Sprites" in file_path
        
def is_player_sprite(file_path):
    return "Assets\\Models\\Players\\Sprites" in file_path

def is_item_sprite (file_path):
    return "Assets\\Models\\Items\\Sprites" in file_path

def is_particle (file_path):
    return "Assets\\Particles" in file_path

def is_sprite (file_path):      
    return "\\Sprites" in file_path


def get_name_without_extension(filename):
    """
    Makes coffee
    Args: 
        filename or fulepath
    """
    new_name_wo_extension = os.path.basename(os.path.splitext(filename)[0])
    return new_name_wo_extension

def get_wave_name(filename):
    """
    Return Wave_blabla    no extension
    Args: 
        filename or fulepath
    """
    name_w_Wave_prefix = f"Wave_{os.path.basename(os.path.splitext(filename)[0])}"
    return name_w_Wave_prefix

def get_bg_name(filename):
    """
    Return Wave_blabla    no extension
    Args: 
        filename or fulepath
    """
    name_w_bg_prefix = f"bg_{os.path.basename(os.path.splitext(filename)[0])}"
    return name_w_bg_prefix

def get_player_name(filename):
    """
    Return Wave_blabla    no extension
    Args: 
        filename or fulepath
    """
    name_w_player_prefix = f"Player_{os.path.basename(os.path.splitext(filename)[0])}"
    return name_w_player_prefix

def get_icon_name(filename):
    """
    Return Icon_blabla    no extension
    Args: 
        filename or fulepath
    """
    new_name_w_iconW_prefix = f"icon_{os.path.basename(os.path.splitext(filename)[0])}"
    return new_name_w_iconW_prefix

def get_icon_filename(filename):
    """
    Return Icon_blabla.png    .png is the difference
    Args: 
        filename or fulepath
    """
    new_filename_w_iconW_prefix = f"icon_{os.path.basename(os.path.splitext(filename)[0])}.png"
    return new_filename_w_iconW_prefix

def get_iconW_name(filename):
    """
    Return IconW_blabla    no extension
    Args: 
        filename or fulepath
    """
    new_name_w_iconW_prefix = f"iconW_{os.path.basename(os.path.splitext(filename)[0])}"
    return new_name_w_iconW_prefix

def get_iconW_filename(filename):
    """
    Return IconW_blabla.png    .png is the difference
    Args: 
        filename or fulepath
    """
    new_filename_w_iconW_prefix = f"iconW_{os.path.basename(os.path.splitext(filename)[0])}.png"
    return new_filename_w_iconW_prefix

def get_Item_name(filename):
    """
    Return IconW_blabla.png    .png is the difference
    Args: 
        filename or fulepath
    """
    new_filename_w_iconW_prefix = f"Item_{os.path.basename(os.path.splitext(filename)[0])}"
    return new_filename_w_iconW_prefix

def get_reference_name (file_path):

    ref_name=""

    if is_background_sprite(file_path):
        ref_name= get_bg_name(file_path)
    elif is_bullet(file_path):
        ref_name= get_name_without_extension(file_path)
    elif is_item_sprite(file_path):
        ref_name= get_Item_name(file_path)
    elif is_enemy_sprite(file_path): 
        ref_name= get_wave_name(file_path)
    elif is_player_sprite(file_path):
        ref_name= get_player_name(file_path)
    elif is_picture(file_path) or is_particle(file_path) or is_sound(file_path) or is_music(file_path):
        ref_name= os.path.basename(file_path) 
        
    return ref_name
    
