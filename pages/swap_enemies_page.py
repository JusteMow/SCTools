import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pour charger et afficher les images
from utils.ui_utils.listbox_levels import ListboxLevels
from tkshared.listbox import ListboxWithSearchAndPreview
import states.states as states
import utils.xml_tools as XT
from pages.base_page import BasePage
from tkshared.general import ScreenNameFilter
import utils.levels_tools as levels_tools
import utils.general_tools as GT
# NoticeLabel is now in states.notice_label


class SwapEnemiesPage(BasePage):
    def __init__(self, root):
        super().__init__(root)

    def create_page(self):
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        # Configure grid layout
        self.page.grid_rowconfigure(0, weight=1)
        self.page.grid_columnconfigure(0, weight=1)  # Swap Enemies
        self.page.grid_columnconfigure(1, weight=1)  # With Enemies
        self.page.grid_columnconfigure(2, weight=1)  # Levels

        # Swap Enemies Listbox
        swap_enemies_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites")
        swap_enemies_data = self.get_enemy_data()
        self.listbox_swap_enemies = ListboxWithSearchAndPreview(
            parent=self.page,
            items=swap_enemies_data,
            preview_dir=swap_enemies_path,
            title="Swap Enemies"
        )
        self.listbox_swap_enemies.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # With Enemies Listbox
        with_enemies_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites")
        with_enemies_data = self.get_enemy_data()
        self.listbox_with_enemies = ListboxWithSearchAndPreview(
            parent=self.page,
            items=with_enemies_data,
            preview_dir=with_enemies_path,
            title="With Enemies"
        )
        self.listbox_with_enemies.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Levels Listbox
        self.levels_listbox = ListboxLevels(
            parent=self.page,
            title="in Levels",
            selectmode=tk.MULTIPLE
        )
        self.levels_listbox.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # ScreenName Filter
        self.screen_name_filter = ScreenNameFilter(parent=self.page)
        self.screen_name_filter.frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Swap Button and Overwrite Checkbox
        swap_frame = tk.Frame(self.page, bg="#2E2E2E")
        swap_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Overwrite Checkbox
        self.overwrite_screen_name_var = tk.BooleanVar(value=True)
        self.overwrite_screen_name_checkbox = tk.Checkbutton(
            swap_frame,
            text="Overwrite screenName",
            variable=self.overwrite_screen_name_var,
            bg="#2E2E2E",
            fg="white",
            selectcolor="#444"
        )
        self.overwrite_screen_name_checkbox.pack(anchor="w", pady=(0, 5))  # Checkbox au-dessus

        # Swap Button
        self.swap_button = tk.Button(
            swap_frame,
            text="Swap Enemies",
            command=self.swap_enemies_func,
            bg="#444",
            fg="white",
            relief="flat"
        )
        self.swap_button.pack(anchor="w")  # Aligner le bouton sous la checkbox

        return self.page
    
    def page_update_items(self):
        super().page_update_items()
        self.listbox_swap_enemies.update_items(self.get_enemy_data())
        self.listbox_with_enemies.update_items(self.get_enemy_data())
        self.levels_listbox.update_items(self.get_levels_data())


    # ============================================== SWAP FUNK =================================================
    def swap_enemies_func(self):
        """
        Main function called when clicking the 'Swap Enemies' button.
        """
        
        # Obtenir l'ennemi à remplacer (Swap Enemies)
        selected_swap_enemy = self.listbox_swap_enemies.get_selected_item()
        
        # Obtenir les informations de l'ennemi dans "With Enemies"
        enemySwapWith_spriteName = self.listbox_with_enemies.get_selected_item()
        if selected_swap_enemy is None or enemySwapWith_spriteName is None:
            states.notice_label.set_text("Please select an enemy to swap in 'Swap Enemies'.", color="red")
            return
        selected_levels = self.levels_listbox.get_selected_items()
        if selected_levels is None:
            states.notice_label.set_text("Please select one or more levels to swap enemies.", color="red")
            return
        
        GT.start_process("Swap ennemies")
        
        # Swap des ennemis dans les niveaux
        levels_tools.swap_enemies_in_levels(selected_levels, 
                                            selected_swap_enemy, 
                                            enemySwapWith_spriteName, 
                                            self.screen_name_filter, 
                                            self.overwrite_screen_name_var.get() 
                                            )
        
        GT.end_process("Swap^Enemies", f"Swap Enemies {os.path.basename(selected_swap_enemy)} -> {os.path.basename(enemySwapWith_spriteName)} in {selected_levels}", True)
        


    

