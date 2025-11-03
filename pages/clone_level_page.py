import os
import tkinter as tk
from tkinter import messagebox
from utils.ui_utils.listbox_levels import ListboxLevels
from pages.base_page import BasePage
import states.states as states
from tkshared.general import EntryPlus
import utils.levels_tools as levels_tools
import utils.xml_tools as XT
import utils.clone_tools as clone_tools
import utils.log_file as log
import utils.general_tools as GT


class CloneLevelPage(BasePage):
    def __init__(self, root):
        super().__init__(root)

    def create_page(self):
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        # Configure grid layout
        self.page.grid_rowconfigure(0, weight=1)
        self.page.grid_columnconfigure(0, weight=1)
        self.page.grid_columnconfigure(1, weight=1)

        # Levels Listbox
        levels_path = os.path.join(states.root_path, "levels")
        self.levels_listbox = ListboxLevels(
            parent=self.page,
            title="Levels",
            selectmode=tk.SINGLE,
            on_select_callback=self.page_on_select_populate_entry
        )
        self.levels_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Clone Configuration
        config_frame = tk.Frame(self.page, bg="#2E2E2E")
        config_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # New Level Name
        tk.Label(config_frame, text="Cloned Level Name:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.new_level_name_var = tk.StringVar()
        self.new_level_name_entry = EntryPlus(config_frame, validation_type="name", textvariable=self.new_level_name_var, bg="#1E1E1E", fg="white",
                                             insertbackground="white", relief="flat", width=30)
        self.new_level_name_entry.pack(fill=tk.X, pady=(0, 10))

        # Clone Enemies as New Objects
        self.clone_enemies_var = tk.BooleanVar(value=False)
        self.clone_enemies_checkbox = tk.Checkbutton(config_frame, text="Clone Enemies as New Objects",
                                                     variable=self.clone_enemies_var, bg="#2E2E2E", fg="white",
                                                     selectcolor="#444", command=self.page_toggle_enemy_cloning_options)
        self.clone_enemies_checkbox.pack(anchor="w", pady=(5, 10))

        # Enemy Prefix/Suffix Options
        self.enemy_options_frame = tk.Frame(config_frame, bg="#2E2E2E")
        self.enemy_options_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(self.enemy_options_frame, text=f"Add Prefix:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        self. prefix_var = tk.StringVar()
        self. prefix_entry = EntryPlus(self.enemy_options_frame, textvariable=self.prefix_var, validation_type="name", bg="#1E1E1E", fg="white", insertbackground="white", relief="flat", width=30)
        self. prefix_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.enemy_options_frame, text=f"Add Suffix:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        self.suffix_var = tk.StringVar()
        self.suffix_entry = EntryPlus(self.enemy_options_frame, textvariable=self.suffix_var, validation_type="name", bg="#1E1E1E", fg="white", insertbackground="white", relief="flat", width=30)
        self.suffix_entry.pack(fill=tk.X, pady=(0, 10))

        # Clone Button
        self.clone_button = tk.Button(config_frame, text="Clone Level", command=self.pre_clone_level,
                                      bg="#444", fg="white", relief="flat")
        self.clone_button.pack(pady=(10, 0))

        self.page_toggle_enemy_cloning_options()

        return self.page

    def page_update_items(self):
        # Reload levels when the page is updated
        levels_data = self.get_levels_data()
        self.levels_listbox.update_items(levels_data)

    def page_toggle_enemy_cloning_options(self):
        """
        Toggles the visibility of enemy cloning options.
        """
        state = tk.NORMAL if self.clone_enemies_var.get() else tk.DISABLED
        for widget in self.enemy_options_frame.winfo_children():
            if isinstance(widget, (tk.Entry, tk.Checkbutton, tk.Button)):
                widget.configure(state=state)

    def page_on_select_populate_entry(self, selected_items):  
        """
        Updates the new name entry based on the selected enemy.
        """
        if selected_items:  # Vérifie que la liste n'est pas vide
            selected_screenName = self.levels_listbox.get_selected_level_screenName()
            # Détermine le nouveau nom avec un suffixe `_clone`
            new_name = f"clone_{selected_screenName}"
            self.new_level_name_var.set(new_name)  # Met à jour le champ d'entrée

    def pre_clone_level(self):
        if self.clone_enemies_var.get() and self.prefix_var.get() == "" and self.suffix_var.get() == "":
            messagebox("prefix or suffix must contain something")
            return
        self.clone_level()


    def clone_level(self):
        """
        Clones a level and optionally its enemies.
        """
        
        GT.start_process("Clone Level")

        # Step 1: Get the selected level
        selected_level_ext = self.levels_listbox.get_selected_item()
        if not selected_level_ext:
            messagebox.showerror("Error", "Please select a level to clone.")
            return
        
        selected_level_number = selected_level_ext[:8]

        # Get the new clone level name
        new_level_number = int(selected_level_number[5:8]) + 1
        clone_level_number = f"level{new_level_number:03d}"
        clone_level_screen_name = self.new_level_name_var.get()

        # Insert the new level
        levels_tools.clone_and_insert_level(selected_level_number, clone_level_number, clone_level_screen_name)

        if self.clone_enemies_var.get():  # If cloning enemies is enabled
            level_path = levels_tools.get_level_filename(clone_level_number)  # Retrieve the path for the selected level
            root = XT.get_root(level_path)  # Parse the XML file

            # Extract enemies to clone, avoiding duplicates
            enemies_to_clone_temp = [enemy.get("spriteName") for enemy in root.findall(".//enemy")]
            enemies_to_clone = list(set(enemies_to_clone_temp))  # Remove duplicates

            for enemy in enemies_to_clone:
                enemy_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites", enemy)
                if not os.path.exists(enemy_path):
                    log.debug (f"{enemy_path} doesn't exist, is it a builit asset pack ? ")
                    continue

                enemy_name, enemy_ext = os.path.splitext(enemy)
                clone_name = (
                    f"{self.prefix_var.get()}{enemy_name}{self.suffix_var.get()}{enemy_ext}"
                )

                # Clone the enemy
                clone_tools.clone_enemy(enemy_path, clone_name, ignore_already_exist=True)

                # Swap the enemy in the cloned level with the newly created or already existing clones
                levels_tools.swap_enemies_in_levels(os.path.basename(level_path), enemy, clone_name, None, True)
            
        states.end_process_log.append(f"end Clone Level : '{selected_level_ext}' cloned as '{clone_level_number}'")
        GT.end_process(f"Clone Level", f"Clone Level : '{selected_level_ext}' cloned as '{clone_level_number}':  Success ! ", True)
        self.page_update_items()


