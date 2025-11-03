import os
import tkinter as tk
from tkinter import messagebox
from utils.ui_utils.listbox_levels import ListboxLevels
from pages.base_page import BasePage
import states.states as states
from tkshared.general import EntryPlus
import utils.levels_tools as level_tools
import utils.log_file as log
import utils.general_tools as GT
# NoticeLabel is now in states.notice_label



class RenameLevelsPage(BasePage):
    def __init__(self, root):
        super().__init__(root)

    def create_page(self):
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        # Configure grid layout for this page
        self.page.grid_rowconfigure(0, weight=1)
        self.page.grid_columnconfigure(0, weight=1)  # Listbox column
        self.page.grid_columnconfigure(1, weight=1)  # Controls column

        # Levels Listbox
        levels_path = os.path.join(states.root_path, "levels")
        # Level Listbox with Screen Names
        self.levels_listbox = ListboxLevels(
            parent=self.page,
            title="Levels",
            selectmode=tk.SINGLE,
        )
        self.levels_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.levels_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Controls Section
        controls_frame = tk.Frame(self.page, bg="#2E2E2E")
        controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Set New Level Number Label
        tk.Label(controls_frame, text="Set New Level Number: (ex 001 ; 012 ; 158)", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))

        # New Level Number Entry
        self.new_level_number_var = tk.StringVar()
        self.new_level_number_entry = EntryPlus(controls_frame, textvariable=self.new_level_number_var, validation_type="format_xxx", bg="#1E1E1E",
                                               fg="white", insertbackground="white", relief="flat", width=30)
        self.new_level_number_entry.pack(fill=tk.X, pady=(0, 10))

        # Set New Level Number Button
        self.set_level_number_button = tk.Button(controls_frame, text="Set New Level Number", command=self.set_new_level_number_func,
                                                 bg="#444", fg="white", relief="flat")
        self.set_level_number_button.pack(pady=10)


        # Set level contiuity Label
        tk.Label(controls_frame, text="Set level con:inuity (restore 001, 002, 003 etc if one is missing)", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))

        # Set level continuity 
        self.set_level_continuity_button = tk.Button(controls_frame, text="Set Level continuity", command=self.set_level_continuity_func,
                                                 bg="#444", fg="white", relief="flat")
        self.set_level_continuity_button.pack(pady=10)

        return self.page

    def page_update_items(self):
        """
        Updates the page when called (e.g., after selecting a new root directory).
        """
        levels_data = self.get_levels_data()
        self.levels_listbox.update_items(levels_data)

    def set_new_level_number_func(self):
        """
        Sets a new level number for the selected level.
        """
        GT.start_process("Change level number")
        selected_level_file = self.levels_listbox.get_selected_item()
        if not selected_level_file:
            states.notice_label.set_text("Please select a level to rename.", "red")
            return

        selected_level = os.path.splitext(selected_level_file)[0]

        new_level_number = self.new_level_number_var.get().strip()
        if not new_level_number.isdigit():
            states.notice_label.set_text( "The new level number must be a valid integer.")
            return


        destination_level= f"level{int(new_level_number):03}"

        level_tools.rename_level_filename(selected_level, destination_level)
  
        GT.end_process ("Change level number", f"rename {selected_level} -> {destination_level} ")
        self.page_update_items()

    def set_level_continuity_func(self):
        """
        Ensure the levels are named sequentially as Level001.level, Level002.level, etc.
        """
        GT.start_process("Set Level Continuity")

        # Get the list of levels in the directory
        levels_dir = os.path.join(states.root_path, "levels")
        levels = sorted(
            [f for f in os.listdir(levels_dir) if f.endswith(".level")],
            key=lambda x: int(x[5:8])  # Extract the numerical part from "levelXXX.level"
        )

        # Iterate over the sorted levels
        for i, level_name in enumerate(levels, start=1):
            # Generate the theoretical level name
            theorical_name = f"level{i:03d}.level"

            # Compare with the current level name
            if level_name != theorical_name:
                
                # Rename the level file
                try:
                    level_tools.rename_level_filename(level_name, theorical_name)
                    print(f"Renamed: {level_name} -> {theorical_name}")
                except Exception as e:
                    print(f"Failed to rename {level_name} -> {theorical_name}: {e}")

        GT.end_process("Set Level Continuity", states.end_process_log)
        self.page_update_items()

