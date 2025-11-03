import os 
import utils.xml_tools as XT

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

 

def rename_enemy_element(element, new_name):
    """
    Args:
        enemy (lxml element) element as lxmlL element
        new_name (str) : new name
    """
    #et donc là, faut vérifier que le element n'est pas une copie. 
    #et normalement on peut tout déduire de enemy et new_name
    #filepath y compris, puisque la fonction est spécifique. sauf, si on l'utilise aussi dans levels. 

    new_name_wo_extension = os.path.splitext(new_name)[0]
    name_w_Wave_prefix = f"Wave_{new_name_wo_extension}"
    new_name_w_iconW_prefix = f"iconW_{new_name_wo_extension}"

    XT.set_property_with_log(element, 'spriteName', new_name)
    XT.set_property_with_log(element, 'waveName', name_w_Wave_prefix)

    toybox = element.find('toybox')
    if toybox is not None:
        XT.set_property_with_log(toybox, 'parentName', name_w_Wave_prefix)
        XT.set_property_with_log(toybox, 'screenName', new_name_wo_extension)
        XT.set_property_with_log(toybox, 'thumbnail', new_name_w_iconW_prefix)

    return element
