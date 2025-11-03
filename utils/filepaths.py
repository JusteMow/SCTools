import os
import states.states as states

class Filepaths:

    def timestamps () : return os.path.join(states.root_path, "gamebox", "files.timeStamps" )
    def background () : return os.path.join(states.root_path, "gamebox","gamebox.background" )
    def bullets () : return os.path.join(states.root_path, "gamebox", "gamebox.bullets" )
    def explosions () : return os.path.join(states.root_path, "gamebox", "gamebox.explosions")
    def items () : return os.path.join(states.root_path, "gamebox", "gamebox.items")
    def materials3d () : return os.path.join(states.root_path, "gamebox", "gamebox.materials3D")
    def pictures () : return os.path.join(states.root_path, "gamebox", "gamebox.pictures" )
    def players () : return os.path.join(states.root_path, "gamebox", "gamebox.players" )
    def sfx () : return os.path.join(states.root_path, "gamebox", "gamebox.sfx")
    def sounds () : return os.path.join(states.root_path, "gamebox", "gamebox.sounds" )
    def sprites () : return os.path.join(states.root_path, "gamebox", "gamebox.sprites" )
    def startmenu () : return os.path.join(states.root_path, "gamebox", "gamebox.startMenu")
    def waves () : return os.path.join(states.root_path, "gamebox", "gamebox.waves" )
    def waypoints () : return os.path.join(states.root_path, "gamebox", "gamebox.waypoints")
    def weapons () : return os.path.join(states.root_path, "gamebox","gamebox.weapons" )

    def levels_path () : return [
        os.path.join(states.root_path, "levels", level_name)
        for level_name in os.listdir(os.path.join(states.root_path, "levels"))
        if level_name.endswith(".level")
    ]

    def particles_path () : return [
        os.path.join(states.root_path, "gamebox", "Cache", "Particles",  particle_name)
        for particle_name in os.listdir(os.path.join(states.root_path, "gamebox", "Cache", "Particles"))
        if not particle_name.endswith("_back")
    ]

    def game_file_path () : return next(
        (os.path.join(states.root_path, file) for file in os.listdir(states.root_path) if file.endswith(".game")),
        None
    )
