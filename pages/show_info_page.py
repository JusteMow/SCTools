import os
import tkinter as tk
from _shared.shared_tkinter_utils.listbox.listbox_with_search import ListboxWithSearch
import utils.xml_tools as XT
import states.states as states
from utils.filepaths import Filepaths


class ShowInfosPage:
    def __init__(self, root):
        self.root = root
        self.page = None
        self.sfx_dict = {}

    def create_page(self):
        """
        Creates the Show Infos page.
        """
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        # Configure grid layout
        self.page.columnconfigure(0, weight=1)
        self.page.columnconfigure(1, weight=1)

        # Left Column: Particles Listbox
        self.particles_listbox = ListboxWithSearch(
            parent=self.page,
            items=[],
            title="Particles",
            on_select_callback=self.on_select_particle
        )
        self.particles_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Right Column: Details Label
        self.all_references_label = tk.Label(
            self.page,
            text="Select a particle to view details",
            bg="#1E1E1E",
            fg="white",
            justify="left",
            anchor="nw",
            font=("Arial", 10),
            wraplength=400
        )
        self.all_references_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.update_items()

        return self.page

    def update_items(self):
        """
        Reads gamebox.sfx and updates the Listbox items.
        """
        sfx_path = os.path.join(states.root_path, "gamebox", "gamebox.sfx")
        root = XT.get_root_in_gamebox(sfx_path)

        self.sfx_dict = {
            sfx.get("screenName"): sfx.get("sfxName")
            for sfx in root.findall(".//SFX")
        }

        self.particles_listbox.update_items(list(self.sfx_dict.keys()))

    def on_select_particle(self, selected_items):
        """
        Handles selection from the Listbox and updates the details label.
        """
        if not selected_items:
            return

  

        selected_screen_name = selected_items[0]
        particle_name = self.sfx_dict.get(selected_screen_name, "Unknown")
        
        #Begin with displaying the particle filename
        all_references = [f"Filename: {particle_name}\n"]


        # Get particles in .game file
        all_references.append(f"\n .game file : ")

        gamefile_path = Filepaths.game_file_path()
        root=XT.get_root(gamefile_path)
        references = self.extract_references_from_gamebox(root, particle_name, "game")
        all_references.extend(references)

        # Get particles in gameBoxes
        gameboxes = ["weapons", "players", "waves", "items", "explosions"]

        for gamebox in gameboxes:

            all_references.append(f"\n {gamebox} : ")

            gamebox_path = getattr(Filepaths, gamebox)()

            root = XT.get_root_in_gamebox(gamebox_path, recover=True)

            references = self.extract_references_from_gamebox(root, particle_name, gamebox)

            all_references.extend(references)

                # Handle levels separately
        level_paths = Filepaths.levels_path()
        for level_path in level_paths:
            root = XT.get_root(level_path)
            references = self.extract_references_from_gamebox(root, particle_name, "levels")
            all_references.extend(references)

 

        # Update Label
        self.all_references_label.config(text="\n".join(all_references))

    def extract_references_from_gamebox(self, root, particle_name, gamebox_type):
        """
        Extract references for a specific particle_name from various gameboxes.

        Args:
            root (ElementTree.Element): The root element of the gamebox.
            particle_name (str): The name of the particle to search for.
            gamebox_type (str): The type of gamebox being processed.

        Returns:
            list: List of references (e.g., screen names) referencing the particle.
        """
        referenced_elements = []

        try:
            if gamebox_type == "weapons":
                for weapon in root.iter("weapon"):
                    attributes_to_check = [
                        weapon.find("name").get("ScreenName", ""),
                        weapon.find("Gameplay").get("hotTimerSfx", ""),
                        weapon.find("Gameplay").get("chargeSfxReadyName", ""),
                        weapon.find("apparence").get("sfxType", ""),
                        weapon.find("apparence").get("impactSfxName", ""),
                        weapon.find("apparence").get("sfxFireName", ""),
                        weapon.find("apparence").get("sfxSmokeName", ""),
                    ]
                    if any(particle_name == attr for attr in attributes_to_check):
                        referenced_elements.append(weapon.find("name").get("ScreenName", "Unknown Weapon"))

            elif gamebox_type == "players":
                for player in root.iter("player"):
                    for sfx in player.findall("SFX"):
                        if sfx.get("sfxName") == particle_name:
                            referenced_elements.append(player.get("playerName", "Unknown Player"))

            elif gamebox_type == "waves":
                for enemy in root.iter("enemy"):
                    attributes_to_check = [
                        enemy.find("Spawner").get("startSfxName", ""),
                    ]
                    for sfx in enemy.findall("SFX"):
                        attributes_to_check.append(sfx.get("sfxName", ""))
                    if any(particle_name == attr for attr in attributes_to_check):
                        referenced_elements.append(enemy.get("waveName", "Unknown Wave"))

            elif gamebox_type == "items":
                for item in root.iter("Item"):
                    attributes_to_check = [
                        item.find("Gameplay").get("ForceFieldSFX", ""),
                        item.find("SFX").get("sfxStartName", ""),
                        item.find("SFX").get("sfxEndName", ""),
                    ]
                    if any(particle_name == attr for attr in attributes_to_check):
                        referenced_elements.append(item.get("itemName", "Unknown Item"))

            elif gamebox_type == "explosions":
                for explosion in root.iter("explosion"):
                    for expl in explosion.findall("EXPL"):
                        if expl.get("particleName") == particle_name:
                            referenced_elements.append(explosion.get("screenName", "Unknown Explosion"))

            elif gamebox_type == "levels":
                for sfx in root.iter("sfx"):
                    particle = sfx.find("particle")
                    if particle is not None and particle.get("particleType") == particle_name:
                        referenced_elements.append(sfx.get("screenName", "Unknown SFX"))

            elif gamebox_type == "game":
                attributes_to_check = [
                    root.find("GFX").get("cancelSfxName", ""),
                    root.find("GFX").get("BGCollisionSfx", ""),
                    root.find("GFX").get("playerCollisionSfx", ""),
                    root.find("GFX").get("playerInvincibleCollisionSfx", ""),
                    root.find("GFX").get("upSfx", "")
                ]
                
                if any(particle_name == attr for attr in attributes_to_check):
                    referenced_elements.append("Game GFX")

        except Exception as e:
            print(f"Error extracting references from {gamebox_type}: {e}")

        return referenced_elements

