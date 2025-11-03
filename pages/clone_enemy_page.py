import os
import tkinter as tk
from tkinter import messagebox
from _shared.shared_tkinter_utils.listbox.listbox_with_search_and_preview import ListboxWithSearchAndPreview
from pages.base_page import BasePage
import states.states as states
from _shared.shared_tkinter_utils.general.entry_plus import EntryPlus
import utils.clone_tools as clone_tools
import utils.general_tools as GT

class CloneEnemyPage(BasePage):
    def __init__(self, root):
        super().__init__(root)

    def create_page(self):
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        # Configure grid layout
        self.page.grid_rowconfigure(0, weight=1)
        self.page.grid_columnconfigure(0, weight=1)
        self.page.grid_columnconfigure(1, weight=1)

        # Enemy Listbox
        enemies_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites")
        enemies_data = self.get_enemy_data()
        self.enemies_listbox = ListboxWithSearchAndPreview(
            parent=self.page,
            items=enemies_data,
            preview_dir=enemies_path,
            title="Enemies",
            on_select_callback=self.update_new_name
        )
        self.enemies_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Clone Section
        self.config_frame = tk.Frame(self.page, bg="#2E2E2E")
        self.config_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # New Name Entry
        tk.Label(self.config_frame, text="New Enemy Name:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        self.new_name_var = tk.StringVar()
        self.new_name_entry = EntryPlus (self.config_frame, textvariable=self.new_name_var, validation_type="name,", bg="#1E1E1E", fg="white",
                                       insertbackground="white", relief="flat", width=30)
        self.new_name_entry.pack(fill=tk.X, pady=(0, 10))

        # Clone Button
        self.clone_button = tk.Button(self.config_frame, text="Clone Enemy", command=self.clone_enemy,
                                      bg="#444", fg="white", relief="flat")
        self.clone_button.pack(pady=(10, 0))
        

        return self.page

    def create_prefix_suffix_fields(self, parent, label_prefix):
        """
        Creates prefix/suffix entry fields for the given label (e.g., Enemy or Weapon).
        """
        tk.Label(parent, text=f"Add {label_prefix} Prefix:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        prefix_var = tk.StringVar()
        prefix_entry = EntryPlus(parent, textvariable=prefix_var, validation_type="name", bg="#1E1E1E", fg="white", insertbackground="white", relief="flat", width=30)
        prefix_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(parent, text=f"Add {label_prefix} Suffix:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        suffix_var = tk.StringVar()
        suffix_entry = EntryPlus(parent, textvariable=suffix_var, validation_type="name", bg="#1E1E1E", fg="white", insertbackground="white", relief="flat", width=30)
        suffix_entry.pack(fill=tk.X, pady=(0, 10))

        return prefix_var, suffix_var

    def page_update_items(self):
        # Reload enemy list when the page is updated
        enemies_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites")
        enemies_data = self.get_enemy_data()
        self.enemies_listbox.update_items(enemies_data)

    def update_new_name(self, selected_items):  
        """
        Updates the new name entry based on the selected enemy.
        """
        if selected_items:  # Vérifie que la liste n'est pas vide
            selected_enemy = selected_items[0]
            # Détermine le nouveau nom avec un suffixe `_clone`
            base_name, ext = os.path.splitext(selected_enemy)
            new_name = f"{base_name}_clone{ext}"
            self.new_name_var.set(new_name)  # Met à jour le champ d'entrée

    #Cloning
    def clone_enemy(self):
        """
        Clones the selected enemy with the new name and updates gamebox.waves.
        """
        GT.start_process("Clone enemy")

        selected_item = self.enemies_listbox.get_selected_item()
        source_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites", selected_item)
        new_name = self.new_name_var.get().strip()

        clone_tools.clone_enemy(source_path, new_name)
        
        GT.end_process(f"Clone enemy", f"Clone {os.path.basename(source_path)} -> {os.path.basename(new_name)}", True)
        self.page_update_items()


