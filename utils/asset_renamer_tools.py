import os
import states.states as states
import utils.log_file as log
import utils.asset_renamer_tools_gamebox as gb
import utils.asset_renamer_tools_level as lvl
import utils.asset_renamer_tools_generic as ar_gen
import utils.general_tools as GT
import utils.gamebox_tools as GB


#===========================================main funk======================================

def rename_asset_func(old_path, new_path, overwrite_screenName, check_cohrence_mode = False):
    """
    Renames an asset across relevant gamebox files, starting with files.timeStamps and handling various gamebox types.

    Args:
        old_path (str): The old asset path to replace.
        new_path (str): The new asset path to insert.

    Returns:
        None
    """
    root_path = states.root_path
    success = True  # Initial success flag
    operation_results = []  # To store the results of operations
    
    log.debug(f"Starting rename_asset process for:\n  Root: {root_path}\n  Old Path: {old_path}\n  New Path: {new_path}")

    # special mode : check coherence mode won't copy files, it checks inside gamebox and levels that asset.png parent is Wave_asset.png
    # and stuff like this. 
    # that's a special case, if you read this, don't mind about this. 
    if not check_cohrence_mode:

        #Handle file rename
        if not GT.rename_file(old_path, new_path):
            return False
            
        #Handle icon file rename
        if not rename_asset_icon_file(old_path, new_path):
            return False

    #get .game file 
    gamefile = GT.get_game_file()
    input_paths = [
    ("GAME.parentPlayerName", ar_gen.NameType.PLAYER_NAME_WO_EXT),
    ("GAME.aimTextureName", ar_gen.NameType.NAME),
    ("SCORING.scoreTextureName", ar_gen.NameType.NAME),
    ("SCORING.multiplierTextureName", ar_gen.NameType.NAME),
    ("GAUGE.GaugeTextureBack", ar_gen.NameType.NAME),
    ("GAUGE.GaugeTextureFront", ar_gen.NameType.NAME),
    ("GAUGE.GaugeTextureReady", ar_gen.NameType.NAME),
    ("CHAINGAUGE.ChainGaugeTextureBack", ar_gen.NameType.NAME),
    ("CHAINGAUGE.ChainGaugeTextureFront", ar_gen.NameType.NAME),
    ("STARTMENU.startMenuBackground", ar_gen.NameType.NAME),
    ("STARTMENU.splashScreenPicture", ar_gen.NameType.NAME),
    ("STARTMENU.splashScreenPicture2", ar_gen.NameType.NAME),
    ("STARTMENU.startMenuLogoGfx", ar_gen.NameType.NAME),
    ("STARTMENU.startMenuBlockTextureName", ar_gen.NameType.NAME),
    ("GAMEMENUS.enemyLifebarTextureBack", ar_gen.NameType.NAME),
    ("GAMEMENUS.enemyLifebarTextureFront", ar_gen.NameType.NAME),
    ("GAMEMENUS.enemyBossLifebarTextureFront", ar_gen.NameType.NAME),
    ("GAMEMENUS.enemyBossLifebarTextureBack", ar_gen.NameType.NAME),
    ("GAMEMENUS.gameOverGfx", ar_gen.NameType.NAME),
    ("GAMEMENUS.gameWinGfx", ar_gen.NameType.NAME),
    ("GAMEMENUS.gameCompletedGfx", ar_gen.NameType.NAME),
    ("GAMEMENUS.gamePauseGfx", ar_gen.NameType.NAME),
    ("GAMEHUD.pauseMenuBG", ar_gen.NameType.NAME),
    ("GAMEHUD.gameHUDBG_texture", ar_gen.NameType.NAME),
    ("GAMEPLAY.smartItemName", ar_gen.NameType.ITEM_NAME_WO_EXT),
    ("GAUGE.gaugeSpawnedItem", ar_gen.NameType.ITEM_NAME_WO_EXT),
    ("GAUGE.gaugeStartSpawnedItem", ar_gen.NameType.ITEM_NAME_WO_EXT),
    ("SOUNDS.startMenuMusic", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicpauseSound", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusiccontinueSound", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicgameOverMusic", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicgameWonMusic", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicgameCompleteMusic", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicstartMenuValidate", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicstartMenuBack", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicstartMenuGo", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicstartMenuClick", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicstartMenuStartsGame", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicSound1up", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicgaugeReadySound", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusicgaugeStartSound", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusiccancelSoundName", ar_gen.NameType.NAME),
    ("SOUNDS.startMenuMusictextSound", ar_gen.NameType.NAME),
    ("HIGHSCOREMENUS.HSspinnerSound", ar_gen.NameType.NAME),
    ("HIGHSCOREMENUS.HSleftRightSound", ar_gen.NameType.NAME),
    ("HIGHSCOREMENUS.HSvalidateSound", ar_gen.NameType.NAME),
    ("HIGHSCOREMENUS.HSMenuBG", ar_gen.NameType.NAME),
    ("HIGHSCOREMENUS.scoreSound", ar_gen.NameType.NAME)
    ]

    #rename_asset_in_gamebox_main(root_path, old_path, new_path)
    ar_gen.rename_asset_in_gamebox_generic(gamefile, input_paths, old_path, new_path)
	
     # Handle files.timeStamps
    success_timeStamps = gb.rename_asset_in_file_timeStamps(old_path, new_path)
    operation_results.append(success_timeStamps)  # Add the result to the list
    log.debug(
        f"Successfully updated references in files.timeStamps for {old_path} -> {new_path}"
        if success_timeStamps
        else f"Failed to update references in files.timeStamps for {old_path} -> {new_path}"
    )

    file_operations = {
        "Assets\\Models\\Bullets": [
            gb.rename_asset_in_gamebox_bullet,
            gb.rename_bullet_asset_in_gamebox_weapons_sprites,
            gb.rename_asset_in_gamebox_sprites
        ],
        "Assets\\Models\\Backgrounds\\Sprites": [
            gb.rename_asset_in_gamebox_background,
        ],
        "Assets\\Sounds\\SoundFX": [
            gb.rename_asset_in_gamebox_explosion,
            gb.rename_asset_in_gamebox_items,
            gb.rename_asset_in_gamebox_players_Sounds,
            gb.rename_asset_in_gamebox_sounds,
            gb.rename_asset_in_gamebox_waves_sounds,
            gb.rename_asset_in_gamebox_waypoints,
            gb.rename_asset_in_gamebox_weapons_sounds,
        ],
        "Assets\\Models\\Items\\Sprites": [
            gb.rename_asset_in_gamebox_items,
        ],
        "Assets\\Pictures": [
            gb.rename_asset_in_gamebox_pictures,
        ],
        "Assets\\Models\\Players\\Sprites": [
            gb.rename_asset_in_gamebox_players_playerSprite,
        ],
        "Assets\\Particles": [
            gb.rename_asset_in_gamebox_explosion,
            gb.rename_particle_asset_in_gamebox_weapons,
            gb.replace_in_particle_cache_files,
            gb.rename_asset_in_gamebox_pictures,
        ],
        "Assets\\Models\\Enemies\\Sprites": [
            gb.rename_asset_in_gamebox_waves_sprites,
        ],
        "Sprites": [
            gb.rename_asset_in_gamebox_sprites,
        ],
    }
	
    # Iterate through gamebox operations
    for path_key, operations in file_operations.items():
        if path_key in old_path:
            for operation in operations:
                success_operation = operation(old_path, new_path)
                operation_results.append(success_operation)
                log.debug(
                    f"Successfully updated references for {operation.__name__} in {old_path} -> {new_path}"
                    if success_operation
                    else f"Failed to update references for {operation.__name__} in {old_path} -> {new_path}"
                )

	#now, levels. 
    success_levels_operations = lvl.rename_asset_in_levels(old_path, new_path, overwrite_screenName)
    operation_results.append(success_levels_operations)  # Add the result to the list

    # Determine overall success
    success = all(result for result in operation_results if result is not None)

    return success

##========================================= Icons ===========================>
def rename_asset_icon_file(old_file_path, new_file_path):
    """
    Renames the icon file associated with a given asset based on its path.

    Args:
        old_file_path (str): The current path of the asset file.
        new_file_path (str): The desired new path of the asset file.
        root_path (str): The root directory of the project.

    Returns:
        bool: True if the icon file was successfully renamed, False otherwise.
    """
    try:
        # Déterminer le dossier des icônes
        icons_path = os.path.join(states.root_path, "gamebox", "icons")

        # Identifier le cas selon le chemin de l'ancien fichier 
        # la différence c'est le W. 
        if "Assets\\Models\\Enemies\\Sprites" in old_file_path:
            icon_old_name = GB.get_iconW_filename(old_file_path)
            icon_new_name = GB.get_iconW_filename(new_file_path)
        elif "Assets\\Models\\Backgrounds\\Sprites" in old_file_path or "Assets\\Models\\Items\\Sprites" in old_file_path:
            icon_old_name = GB.get_icon_filename(old_file_path)
            icon_new_name = GB.get_icon_filename(new_file_path)
        else:
            log.debug(f"No icons")
            return True

        # Construire les chemins complets des fichiers d'icônes
        old_icon_full_path = os.path.join(icons_path, icon_old_name)
        new_icon_full_path = os.path.join(icons_path, icon_new_name)

        GT.rename_file(old_icon_full_path, new_icon_full_path)
        return True

    except Exception as e:
        states.set_error_found(f"Error renaming icon file: {e}")
        return False


