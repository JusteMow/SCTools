import tkinter as tk
import os
import utils.xml_tools as XT
import states.states as states
from _shared.shared_tkinter_utils.listbox.listbox_with_search import ListboxWithSearch


class ListboxLevels(ListboxWithSearch):
    def __init__(self, parent, title, selectmode=tk.SINGLE, on_select_callback=None):
        """
        Initializes a searchable listbox specifically for levels.

        Args:
            parent (tk.Widget): Parent widget (frame or root).
            levels_path (str): Path to the levels directory.
            title (str): Title displayed above the listbox.
            selectmode (tk.SelectMode): SINGLE or MULTIPLE selection mode.
            on_select_callback (function): Callback triggered on selection.
        """
        self.levels_path = os.path.join(states.root_path, "levels")
        self.levels_data = self.get_levels_with_screen_names()
        super().__init__(parent, self.levels_data, title, selectmode, on_select_callback)

    def get_levels_with_screen_names(self):
        """
        Retrieves levels with their screen names.

        Returns:
            list: List of formatted level names with screen names.
        """
        levels_with_titles = []
        if os.path.exists(self.levels_path):
            for file in os.listdir(self.levels_path):
                if file.endswith(".level") and os.path.isfile(os.path.join(self.levels_path, file)):
                    file_path = os.path.join(self.levels_path, file)
                    try:
                        root = XT.get_root(file_path)
                        level_node = root.find("Level")
                        screen_title = level_node.get("screenName") if level_node is not None else "(No Title)"
                        display_name = f"{file} - {screen_title}"
                        levels_with_titles.append(display_name)
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")
        return levels_with_titles

    def update_items(self, item):
        """
        Mainly a callback function called when on root_path update
        Reloads the level data with screen names.
        """
        self.levels_data = self.get_levels_with_screen_names()
        super().update_items(self.levels_data)

    def get_selected_items(self):
        """
        Returns the LIST of selected levels without their names as : [Level000.level, level004.level]
        """
        selected_indices = self.listbox.curselection()
        # Retourne les 8 premiers caractères pour chaque élément sélectionné
        return [self.filtered_items[i][:14] for i in selected_indices]
    
    def get_selected_item(self):
        """
        Returns the selected Level levels without its name as : level000.level
        """
        return self.get_selected_items()[0]
    
    def get_selected_levels_screenNames(self):
        """
        Returns the LIST of selected levels ScreenNames
        """
        selected_indices = self.listbox.curselection()
        # Retourne les 8 premiers caractères pour chaque élément sélectionné
        return [self.filtered_items[i][16:] for i in selected_indices]

    def get_selected_level_screenName(self):
        """
        Returns the selected level ScreenName
        """
        return self.get_selected_levels_screenNames()[0]