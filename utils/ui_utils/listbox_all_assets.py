import tkinter as tk
import os
from _shared.shared_tkinter_utils.listbox.listbox_with_search_and_preview import ListboxWithSearchAndPreview
import utils.general_tools as GT
import states.states as states

class ListboxAllAssets(ListboxWithSearchAndPreview):
    def __init__(self, parent, items, preview_dir, title, selectmode=tk.SINGLE, on_select_callback=None):
        """
        A simplified Listbox inheriting from ListboxWithSearchAndPreview.
        
        Args:
            parent (tk.Widget): Parent widget.
            items (list): List of asset paths.
            preview_dir (str): Directory for preview images.
            title (str): Title for the listbox.
            selectmode (tk.SelectMode): Selection mode (SINGLE or MULTIPLE).
            on_select_callback (function): Callback triggered on selection.
        """
        self.filters = {
            "show_path" :tk.BooleanVar(value=True),
            "show_problems_only": tk.BooleanVar(value=False),
            "show_backgrounds": tk.BooleanVar(value=True),
            "show_bullets": tk.BooleanVar(value=True),
            "show_enemies": tk.BooleanVar(value=True),
            "show_items": tk.BooleanVar(value=True),
            "show_particles": tk.BooleanVar(value=True),
            "show_pictures": tk.BooleanVar(value=True),
            "show_players": tk.BooleanVar(value=True),
            "show_sounds": tk.BooleanVar(value=True),
        }
        self.assets_issues = {}
        # Filters frame
        filter_frame = tk.Frame(parent, bg="#2E2E2E", height=100)
        filter_frame.pack(side="top", fill="x", pady=(5, 0))
        filter_frame.pack_propagate(False)  # Fix height to 100 pixels

        for idx, (key, var) in enumerate(self.filters.items()):
            tk.Checkbutton(
                filter_frame, text=key.replace("_", " ").title(), variable=var,
                command=self.private_update_listbox, bg="#2E2E2E", fg="white", selectcolor="#444"
            ).grid(row=idx // 3, column=idx % 3, sticky="w", padx=10)

        # Listbox frame
        lb_frame = tk.Frame(parent, bg="#2E2E2E")
        lb_frame.pack(side="top", fill="both", expand=True, pady=(0, 5))

        super().__init__(lb_frame, items, preview_dir, title, selectmode, on_select_callback)

    # Listbox will only display filtered assets
    def private_update_listbox(self, *args):
        self.detect_all_assets_filenames_issues()

        self.filter_items()
        

        self.listbox.delete(0, tk.END)

        for item in self.filtered_items:

            relative_path = os.path.relpath(item, states.root_path)
            displayed_name = relative_path if self.filters["show_path"].get() else os.path.basename(item)

            self.listbox.insert(tk.END, displayed_name)
            if "space" in self.assets_issues[item]:
                self.listbox.itemconfig(tk.END, {"bg": "red", "fg": "white"})

            elif "conflict" in self.assets_issues[item]:
                self.listbox.itemconfig(tk.END, {"bg": "yellow", "fg": "black"})

    def filter_items(self):
        """
        Override the base function to search in filename not path
        Filters the listbox items based on the search term and custom rules.
        """
        self.filtered_items = []
        
        search_term = self.search_var.get().lower()

        for item in self.items:

            if not search_term in os.path.basename(item).lower():
                continue
            if self.filters["show_problems_only"].get() and not self.assets_issues[item]:
                continue
            if not self.filters["show_backgrounds"].get() and "Assets\\Models\\Backgrounds" in item:
                continue
            if not self.filters["show_bullets"].get() and "Assets\\Models\\Bullets" in item:
                continue
            if not self.filters["show_enemies"].get() and "Assets\\Models\\Enemies" in item:
                continue
            if not self.filters["show_items"].get() and "Assets\\Models\\Items" in item:
                continue
            if not self.filters["show_particles"].get() and "Assets\\Particles" in item:
                continue
            if not self.filters["show_pictures"].get() and "Assets\\Pictures" in item:
                continue
            if not self.filters["show_players"].get() and "Assets\\Models\\Players" in item:
                continue
            if not self.filters["show_sounds"].get() and "Assets\\Sounds" in item:
                continue

            self.filtered_items.append(item)


    def detect_all_assets_filenames_issues(self):
        self.assets_issues = {} #is a dictionnary 

        self.conflict_names = GT.detect_all_asset_name_conflict()

        for asset in self.items:
            base_name = os.path.splitext(os.path.basename(asset))[0]
            
            #set a new key in dictionnary
            self.assets_issues[asset] = []
            if " " in base_name:
                self.assets_issues[asset].append("space")

            if self.conflict_names[base_name] > 1:
                self.assets_issues[asset].append("conflict")

        return self.assets_issues
    

