import os
import tkinter as tk
from tkinter import messagebox
from utils.ui_utils.listbox_levels import ListboxLevels
from _shared.shared_tkinter_utils.listbox.listbox_with_search_and_preview import ListboxWithSearchAndPreview
from _shared.shared_tkinter_utils.general.screen_name_filter import ScreenNameFilter
from pages.base_page import BasePage
import states.states as states
import utils.xml_tools as XT
from _shared.shared_tkinter_utils.general.entry_plus import EntryPlus
import utils.general_tools as GT
import utils.gamebox_tools as GB
import utils.log_file as log
# NoticeLabel is now in states.notice_label


class SetEnemyPropsPage(BasePage):
    def __init__(self, root):
        super().__init__(root)

    def create_page(self):
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        #Left PAnel 
        # Configure grid layout for this page
        self.page.grid_rowconfigure(0, weight=1)  # Allow rows to stretch
        self.page.grid_columnconfigure(0, weight=1)  # Allow column 0 to stretch
        self.page.grid_columnconfigure(1, weight=1)  # Allow column 1 to stretch
        self.page.grid_columnconfigure(2, weight=1)  # Allow column 2 to stretch

        # Enemies Listbox with Search and Preview
        enemies_path = os.path.join(states.root_path, "Assets", "Models", "Enemies", "Sprites")
        enemies_data = self.get_enemy_data()
        self.enemies_listbox = ListboxWithSearchAndPreview(parent=self.page, items=enemies_data, preview_dir=enemies_path,
                                                           title="Enemies")
        self.enemies_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # ScreenName Filter under Enemies Listbox
        self.screen_name_filter = ScreenNameFilter(parent=self.page)
        self.screen_name_filter.frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Mid Panel

        # Levels Listbox with Search
        self.levels_listbox = ListboxLevels(parent=self.page, title="in Levels", selectmode=tk.MULTIPLE)
        self.levels_listbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # All Levels Checkbox
        levels_controls_frame = tk.Frame(self.page, bg="#2E2E2E")
        levels_controls_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Frame for props
        properties_set_frame = tk.Frame(levels_controls_frame, bg="#2E2E2E")
        properties_set_frame.pack(anchor="w", pady=10, fill="x")

        # invisible Checkbox
        self.is_invisible_var = tk.BooleanVar(value=False)
        self.is_invisible_checkbox = tk.Checkbutton(properties_set_frame, text="is invisible",
                                                       variable=self.is_invisible_var, bg="#2E2E2E",
                                                       fg="white", selectcolor="#444")
        self.is_invisible_checkbox.pack(side="left", padx=5)

        # Set Button Invisible
        self.set_is_invisible_button = tk.Button(properties_set_frame, text="Set",
                                                    command=lambda: self.set_enemy_property("visibility"), bg="#444",
                                                    fg="white", relief="flat", width=10)
        self.set_is_invisible_button.pack(side="left", padx=10)

        # Cancels Bullets on Death Checkbox
        self.cancels_bullets_var = tk.BooleanVar(value=False)
        self.cancels_bullets_checkbox = tk.Checkbutton(properties_set_frame, text="Cancels Bullets on Death",
                                                       variable=self.cancels_bullets_var, bg="#2E2E2E",
                                                       fg="white", selectcolor="#444")
        self.cancels_bullets_checkbox.pack(side="left", padx=5)

        # Set Button Cancel Bullets
        self.set_cancels_bullets_button = tk.Button(properties_set_frame, text="Set",
                                                    command=lambda: self.set_enemy_property("bullet cancel"), bg="#444",
                                                    fg="white", relief="flat", width=10)
        self.set_cancels_bullets_button.pack(side="left", padx=10)

        # Right Panel 

        # Items Listbox with Search and Preview
        items_path = os.path.join(states.root_path, "Assets", "Models", "Items", "Sprites")
        items_data = self.get_items_data()
        self.items_listbox = ListboxWithSearchAndPreview(parent=self.page, items=items_data, preview_dir=items_path,
                                                         title="Items")
        self.items_listbox.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Fields under Items Listbox
        items_fields_frame = tk.Frame(self.page, bg="#2E2E2E")
        items_fields_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Item Number
        tk.Label(items_fields_frame, text="Item Number:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=2)
        self.item_number_var = tk.StringVar(value = 1)
        self.item_number_entry = EntryPlus(items_fields_frame, textvariable=self.item_number_var, validation_type="positive_integer", bg="#1E1E1E", fg="white",
                                          relief="flat", insertbackground="white")
        self.item_number_entry.pack(fill="x", pady=2)

        # Item Radius
        tk.Label(items_fields_frame, text="Item Radius:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=2)
        self.item_radius_var = tk.StringVar(value = 10)
        self.item_radius_entry = EntryPlus(items_fields_frame, textvariable=self.item_radius_var, validation_type="positive_float", bg="#1E1E1E", fg="white",
                                          relief="flat", insertbackground="white")
        self.item_radius_entry.pack(fill="x", pady=2)

        # Item Random
        tk.Label(items_fields_frame, text="Item Random:", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=2)
        self.item_random_var = tk.StringVar(value = .5)
        self.item_random_entry = EntryPlus(items_fields_frame, textvariable=self.item_random_var, validation_type="float_0_1", bg="#1E1E1E", fg="white",
                                          relief="flat", insertbackground="white")
        self.item_random_entry.pack(fill="x", pady=2)

        # Each Copies Spawn Item Checkbox
        self.each_copies_var = tk.BooleanVar(value=False)
        self.each_copies_checkbox = tk.Checkbutton(items_fields_frame, text="Each Copies Spawn Item", variable=self.each_copies_var,
                                                   bg="#2E2E2E", fg="white", selectcolor="#444")
        self.each_copies_checkbox.pack(anchor="w", pady=5)

        # Assign Items Button
        self.assign_items_button = tk.Button(items_fields_frame, text="Assign Items", command=self.Assign_items_func,
                                             bg="#444", fg="white", relief="flat")
        self.assign_items_button.pack(pady=10)

        return self.page

    def get_items_data(self):
        """
        Retrieve item asset names from the Assets directory.
        """
        items_path = os.path.join(states.root_path, "Assets", "Models", "Items", "Sprites")
        data = []
        if os.path.exists(items_path):
            for file in os.listdir(items_path):
                if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    data.append(file)
        return data
    
    def page_update_items(self):
        """
        Update the page when the root path or other state changes.
        """
        self.enemies_listbox.update_items(self.get_enemy_data())
        self.items_listbox.update_items(self.get_items_data())
        self.levels_listbox.update_items(self.get_levels_data())

    def private_validate_items_set_launch(self):
        """
        Prevalidates that item selection is ok.
        """
        self.selected_item = self.items_listbox.get_selected_item()
        if self.selected_item is None:
            states.notice_label.set_text("Please select an item from the 'Items' list.", color="red")
            return False
        
        try:
            self.item_number = int(self.item_number_entry.get())
            if self.item_number < 0:
                raise ValueError("Item number must be a positive integer.")
        except ValueError:
            states.notice_label.set_text("Item number must be a positive integer.", color="red")
            return False

        try:
            self.item_radius = float(self.item_radius_entry.get())
            if self.item_radius < 0:
                raise ValueError("Item radius must be a positive number.")
        except ValueError:
            states.notice_label.set_text("Item radius must be a positive number.", color="red")
            return False

        try:
            self.item_random = float(self.item_random_entry.get())
            if not (0 <= self.item_random <= 1):
                raise ValueError("Item random must be between 0 and 1.")
        except ValueError:
            states.notice_label.set_text( "Item random must be between 0 and 1.", color="red")
            return False
        
        return True
    
    def private_validate_levels_and_enemy(self):
        """
        Prevalidates that enemy and levels selection are ok.
        """
        # Récupérer les sélections utilisateur
        selected_enemy = self.enemies_listbox.get_selected_item()
        print (self.enemies_listbox.get_selected_items())
        if selected_enemy is None:
            states.notice_label.set_text("Please select an enemy from the 'Enemies' list.", color="red")
            return False
        
        # Récupérer les niveaux sélectionnés
        selected_levels = self.levels_listbox.get_selected_items()
        if not selected_levels:
            states.notice_label.set_text("Please select one or more levels to update.", color="red")
            return False

        return True

    def Assign_items_func(self):
        """
        Assigns items to selected enemies in selected levels based on user inputs.
        """

        if not self.private_validate_items_set_launch() or not self.private_validate_levels_and_enemy():
            return

        GT.start_process("Assign Item")

        selected_enemy = self.enemies_listbox.get_selected_item()
        selected_levels = self.levels_listbox.get_selected_items()
        all_spawn = self.each_copies_var.get()

        levels_path = os.path.join(states.root_path, "levels")

        total_updates = 0

        new_log_entry= []

        try:
            for level_file in selected_levels:
                level_path = os.path.join(levels_path, level_file)

                if not os.path.exists(level_path):
                    log.debug(f"Level file not found: {level_path}")
                    continue

                # Parse the XML file
                root = XT.get_root(level_path)
                enemies_updated = 0

                # Iterate over enemies in the level
                for enemy in root.iter('enemy'):
                    sprite_name = enemy.get("spriteName")
                    if sprite_name == selected_enemy:
                        screen_name = enemy.find("toybox").get("screenName")
                        if not self.screen_name_filter.match_filter(screen_name):
                            continue

                        # Find or create ITEMS element
                        items_element = enemy.find("ITEMS")
                        if items_element is None:
                            continue

                        # Set the item properties
                        XT.set_property_with_log(items_element, "itemSpawned", GB.get_Item_name(self.selected_item))
                        XT.set_property_with_log(items_element, "itemNumber", str(self.item_number))
                        XT.set_property_with_log(items_element, "itemRadius", str(self.item_radius))
                        XT.set_property_with_log(items_element, "itemRandom", str(self.item_random))
                        XT.set_property_with_log(items_element, "isEachCopiesSpawnItem", str(all_spawn).lower())

                        enemies_updated += 1
                        total_updates += 1

                if enemies_updated > 0:
                    # Write updated content back to the file
                    XT.write_updated_content(level_path, root)
                    new_log_entry.append("File updated successfully: {level_file}")



        except Exception as e:
            states.set_error_found("Error", f"Failed to assign items to enemies: {e}")

        self.page_update_items()
        
        log_entry = "Success", (f"Items assigned successfully! {total_updates} updates made." 
                                if total_updates > 0 
                                else f"No matching enemies found to update in selected levels.")
        GT.end_process("Assign Item", log_entry)

    def set_cancels_bullets(self):
        if not  self.private_validate_levels_and_enemy():
            return

        GT.start_process(f"set cancel cullet on death to {self.cancels_bullets_var.get()}")
        
        levels_path = os.path.join(states.root_path, "levels")

        selected_enemy = self.enemies_listbox.get_selected_item()
        selected_levels = self.levels_listbox.get_selected_items()

        total_updates = 0

        new_log_entry= []

        try:
            for level_file in selected_levels:
                level_path = os.path.join(levels_path, level_file)

                if not os.path.exists(level_path):
                    log.debug(f"Level file not found: {level_path}")
                    continue

                # Parse the XML file
                root = XT.get_root(level_path)
                enemies_updated = 0

                # Iterate over enemies in the level
                for enemy in root.iter('enemy'):
                    sprite_name = enemy.get("spriteName")
                    if sprite_name == selected_enemy:
                        screen_name = enemy.find("toybox").get("screenName")
                        if not self.screen_name_filter.match_filter(screen_name):
                            continue

                        XT.set_property_with_log(enemy, "isHiddenEnemy", str(self.cancels_bullets_var.get()).lower())

                        enemies_updated += 1
                        total_updates += 1

                if enemies_updated > 0:
                    # Write updated content back to the file
                    XT.write_updated_content(level_path, root)
                    new_log_entry.append("File updated successfully: {level_file}")



        except Exception as e:
            states.set_error_found("Error", f"Failed to assign items to enemies: {e}")

        self.page_update_items()
        
        log_entry = "Success", (f"Items assigned successfully! {total_updates} updates made." 
                                if total_updates > 0 
                                else f"No matching enemies found to update in selected levels.")
        GT.end_process(f"set cancel cullet on death to {self.cancels_bullets_var.get()}", log_entry)

    
    
    def set_enemy_property(self, process_name):
        if not self.private_validate_levels_and_enemy():
            return
        
        process_title = (f"set bullet cancel on death to {self.cancels_bullets_var.get()}" 
                         if process_name == "bullet cancel"
                         else f"set enemy invisible to {self.is_invisible_var.get()}")
        GT.start_process(f"{process_name} to {process_title}")
        
        levels_path = os.path.join(states.root_path, "levels")

        selected_enemy = self.enemies_listbox.get_selected_item()
        selected_levels = self.levels_listbox.get_selected_items()

        total_updates = 0
        new_log_entry = []

        try:
            for level_file in selected_levels:
                level_path = os.path.join(levels_path, level_file)

                if not os.path.exists(level_path):
                    log.debug(f"Level file not found: {level_path}")
                    continue

                # Parse the XML file
                root = XT.get_root(level_path)
                enemies_updated = 0

                # Iterate over enemies in the level
                for enemy in root.iter('enemy'):
                    sprite_name = enemy.get("spriteName")
                    if sprite_name == selected_enemy:
                        screen_name = enemy.find("toybox").get("screenName")
                        if not self.screen_name_filter.match_filter(screen_name):
                            continue

                        if process_name == "bullet cancel":
                            # Set the property dynamically
                            XT.set_property_with_log(enemy.find("GAMEPLAY"), "isDeathCancelsBullets", str(self.cancels_bullets_var).lower())
                        elif process_name == "visibility":
                            XT.set_property_with_log(enemy, "isHiddenEnemy", str(self.is_invisible_var.get()).lower())

                        enemies_updated += 1
                        total_updates += 1

                if enemies_updated > 0:
                    # Write updated content back to the file
                    XT.write_updated_content(level_path, root)
                    new_log_entry.append(f"File updated successfully: {level_file}")

        except Exception as e:
            states.set_error_found(f"Error", f"Failed to update: {e}")

        self.page_update_items()
        
        log_entry = (
            "Success",
            f"{process_name} successfully! {total_updates} updates made."
            if total_updates > 0
            else f"No matching enemies found to update in selected levels."
        )
        GT.end_process(process_title, log_entry)




