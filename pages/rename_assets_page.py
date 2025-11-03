import os
import tkinter as tk
from tkinter import messagebox
import states.states as states
from pages.base_page import BasePage
import utils.asset_renamer_tools as asset_renamer_tools
from tkshared.general import EntryPlus
import utils.general_tools as GT
from utils.ui_utils.listbox_all_assets import ListboxAllAssets
import utils.log_file as log
# NoticeLabel is now in states.notice_label
import utils.extract_assets_tools as extract_assets_tools
import utils.ui_utils.progress_bar as ui_progress_bar

class RenameAssetsPage(BasePage):
    def __init__(self, root):
        super().__init__(root)
        self.filename_var = tk.StringVar()
        self.overwrite_screen_name_var = tk.BooleanVar(value=True)
        self.assets_listbox = None  # Initialize as None

    def create_page(self):
        """
        Creates the Rename Assets page with ListboxAllAssets on the left and controls on the right.
        """
        self.page = tk.Frame(self.root, bg="#2E2E2E")

        # Left Frame for ListboxAllAssets
        left_frame = tk.Frame(self.page, bg="#2E2E2E", width=666)  # Approximately 2/3 of 1000px width
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        self.assets_listbox = ListboxAllAssets(
            parent=left_frame, items=GT.get_all_assets(), preview_dir=states.root_path, title="Assets",
            on_select_callback=self.page_on_asset_select, selectmode=tk.EXTENDED
        )
        self.assets_listbox.pack(fill="both", expand=True)

        # Right Frame for controls
        right_frame = tk.Frame(self.page, bg="#2E2E2E", width=334)  # Approximately 1/3 of 1000px width
        right_frame.pack(side=tk.LEFT, fill="both", expand=False, padx=10, pady=10)

        # Center content vertically
        right_frame.pack_propagate(False)
        content_frame = tk.Frame(right_frame, bg="#2E2E2E")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", x=10)
        

        # Title for tools
        tk.Label(content_frame, text="File Name Tools", bg="#2E2E2E", fg="white", font=("Arial", 12)).pack(pady=(0, 10))
        
        # Rename Section
        tk.Label(content_frame, text="Rename", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w")
        self.filename_entry = EntryPlus(
            content_frame, textvariable=self.filename_var, validation_type="name", width=30, bg="#1E1E1E",
            fg="white", insertbackground="white", relief="flat"
        )
        self.filename_entry.pack(pady=5, fill="x")
        self.rename_button = tk.Button(
            content_frame, text="Rename", command=self.prepare_rename_asset_func, bg="#444", fg="white", relief="flat",
        )
        self.rename_button.pack(pady=5, fill="x")

        # Frame for prefix entries
        prefix_frame = tk.Frame(content_frame, bg="#2E2E2E")
        prefix_frame.pack(fill="x", pady=(10, 5))

        # Label and EntryPlus for prefix to replace
        tk.Label(prefix_frame, text="Old Prefix", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.old_prefix_var = tk.StringVar()
        self.old_prefix_entry = EntryPlus(
            prefix_frame, textvariable=self.old_prefix_var, validation_type="name", width=15, bg="#1E1E1E",
            fg="white", insertbackground="white", relief="flat"
        )
        self.old_prefix_entry.pack(side="left", padx=(0, 10))

        # Label and EntryPlus for new prefix
        tk.Label(prefix_frame, text="New Prefix", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        self.new_prefix_var = tk.StringVar()
        self.new_prefix_entry = EntryPlus(
            prefix_frame, textvariable=self.new_prefix_var, validation_type="name", width=15, bg="#1E1E1E",
            fg="white", insertbackground="white", relief="flat"
        )
        self.new_prefix_entry.pack(side="left")

        # Button for applying prefix
        tk.Button(
            content_frame, text="Apply Prefix", command=self.apply_prefix_func, bg="#444", fg="white", relief="flat",
        ).pack(pady=5, fill="x")

        # Remove Spaces Section
        tk.Label(content_frame, text="Remove Spaces", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(10, 0))
        tk.Button(
            content_frame, text="Replace all spaces with _", command=self.replace_spaces_with_underscores_func,
            bg="#444", fg="white", relief="flat",
        ).pack(pady=5, fill="x")

        # Apply snake_case convention names
        tk.Label(content_frame, text="apply_snake_case_convention_names", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(10, 0))
        tk.Button(
            content_frame, text="apply_snake_case_convention_names", command=self.apply_snake_case_convention_name, bg="#444",
            fg="white", relief="flat",
        ).pack(pady=5, fill="x")

        # Extract Unused Assets Section
        tk.Label(content_frame, text="Extract All Unused Assets", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(10, 0))
        tk.Button(
            content_frame, text="Extract All Unused Assets", command=self.extract_unused_assets_func, bg="#444",
            fg="white", relief="flat",
        ).pack(pady=5, fill="x")

        # Check name coherence 
        tk.Label(content_frame, text="Check assets cohernce inside files", bg="#2E2E2E", fg="white", font=("Arial", 10)).pack(anchor="w", pady=(10, 0))
        tk.Button(
            content_frame, text="Check assets cohernce inside files", command=self.check_name_coherence, bg="#444",
            fg="white", relief="flat",
        ).pack(pady=5, fill="x")

        # Info Text
        info_text = (
            "- Won't work with 3D objects or background, because I don't have any.\n"
            "- Always backup before editing.\n"
            "- Use at your own risk (should be fine).\n"
            "- If you find bugs, contact me!"
        )
        tk.Label(content_frame, text=info_text, bg="#2E2E2E", fg="white", font=("Arial", 8), justify="left").pack(pady=(10, 0))

        self.page_update_items()

        return self.page

    def page_update_items(self):
        """
        Updates the page and reloads the assets.
        """
        super().page_update_items()
        if states.root_path:
            self.assets_listbox.update_items(GT.get_all_assets())
            states.notice_label.set_text("Ready !", "yellow")

    def page_on_asset_select(self, selected_items):
        """
        Callback for when an asset is selected in the listbox.
        """
        if selected_items:
            selected_asset = selected_items[0]
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, os.path.basename(selected_asset))

    def prepare_rename_asset_func(self):
        self.private_validate_new_name()

        GT.start_process("Rename Asset")

        selected_item = self.assets_listbox.get_selected_item()
        if selected_item is None :
            messagebox.showerror("Error", "No asset selected.")
            return
        old_path = selected_item
        new_name = self.filename_var.get()
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        asset_renamer_tools.rename_asset_func(old_path, new_path, self.overwrite_screen_name_var.get())

        self.assets_listbox.update_items(GT.get_all_assets())

        GT.end_process("Rename Assets", f"{os.path.basename(old_path)} -> {os.path.basename(new_path)}", True)

    def private_validate_new_name(self, *args):
        if not self.filename_var.get():
            return False
        
        #validate selected item
        if len(self.assets_listbox.get_selected_items()) > 1:
            states.notice_label.set_text("Mutiple assets selected, select only one", "red")
            
            return False

        selected_asset = self.assets_listbox.get_selected_item()
        if not selected_asset:
            return False

        #validates new name
        new_name = self.filename_var.get()

        if not GT.validate_extension(new_name):
            states.notice_label.set_text("The name extension not valid", "red")
            return False
        
        if new_name == os.path.basename(selected_asset):
            states.notice_label.set_text("Set a new name", "red")
            return False

        suggested_name = GT.validate_new_filename_or_get_another(new_name)

        if suggested_name != new_name:
            states.notice_label.set_text("The name already exists, suggestion added", "red")
            self.filename_var.set(suggested_name)
            return False

        return True
    
    def apply_prefix_func(self):
        """
        Apply prefix to all files, unless it already have same prefix
        If a conflict occurs, stops the process and highlights the conflicting asset.
        """
        if self.assets_listbox.get_selected_items() is None:
            states.notice_label.set_text("Select assets first", color="red")
            return
        
        GT.start_process("replace space with _ ")

        for asset_path in self.assets_listbox.get_selected_items():
            # Check if the asset has a space in its name
            if " " in asset_path:
                new_path_auto = GT.validate_new_filename_or_get_another(
                    self.private_replace_and_add_prefix_get_name(self.old_prefix_var.get(),
                        self.new_prefix_var.get(),
                        asset_path)
                )
                self.private_rename_file(asset_path, new_path_auto)

        # Refresh the listbox after processing
        self.assets_listbox.update_items(GT.get_all_assets())

        GT.end_process("replace space with _ ", states.end_process_log, True)

    def private_replace_and_add_prefix_get_name(self, old_prefix, new_prefix, file_path):
        """
        Replace an old prefix with a new prefix in the filename.

        Args:
            old_prefix (str): The prefix to replace. If empty, no prefix is removed.
            new_prefix (str): The new prefix to add to the filename.
            file_path (str): The full path to the file.

        Returns:
            str: The new file path with the updated prefix.
        """
        # Get the directory and filename
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        # Remove the old prefix if it exists
        if filename.lower().startswith(old_prefix.lower()):
            filename = filename[len(old_prefix):]

        # Add the new prefix
        updated_filename = f"{new_prefix}{filename}"

        # Return the new file path
        return os.path.join(directory, updated_filename)
    
    def replace_spaces_with_underscores_func(self):
        """
        Replaces all spaces in asset names with underscores.
        If a conflict occurs, stops the process and highlights the conflicting asset.
        """
        if self.assets_listbox.get_selected_items() is None:
            states.notice_label.set_text("Select assets first", color="red")
            return
        
        GT.start_process("Replace spaces with _")
        
        for asset_path in self.assets_listbox.get_selected_items():
            # Check if the asset has a space in its name
            if " " in os.path.basename(asset_path):
                new_path_auto = GT.validate_new_filename_or_get_another(asset_path)
                
                self.private_rename_file(asset_path, new_path_auto)

        # Refresh the listbox after processing
        self.assets_listbox.update_items(GT.get_all_assets())

        # Générer les messages de log pour impression
        log_messages = "no files with space found" if states.end_process_log == [] else "\n".join( [
            log_line
            for log_line in states.end_process_log
        ])
        
        GT.end_process("Replace spaces with _", log_messages, True)
            


    def apply_snake_case_convention_name(self):
        """
        replace all names with the snake_case to avoid the asset1.png to be after ZZZ_zzzaset2.png 
        """
        if self.assets_listbox.get_selected_items() is None:
            states.notice_label.set_text("Select assets first", color="red")
            return
        
        GT.start_process("Replace spaces with _")

        for asset_path in self.assets_listbox.get_selected_items():
            
            # save log 

            snake_name = GT.validate_new_filename_or_get_another(GT.convert_to_snake_case(os.path.basename(asset_path)))

            if snake_name != os.path.basename(asset_path):

                old_path = asset_path
                new_path = os.path.join(os.path.dirname(asset_path), snake_name)
                
                self.private_rename_file(old_path, new_path)

        # Refresh the listbox after processing
        self.assets_listbox.update_items(GT.get_all_assets())

        # Générer les messages de log pour impression
        log_messages = "no files with space found" if states.end_process_log == [] else "\n".join( [
            log_line
            for log_line in states.end_process_log
        ])
        
        GT.end_process("Replace spaces with _", log_messages, True)

    #Handle the rename operation, the log entru, and progress bar which doesn't work anyway
    def private_rename_file(self, old_path, new_path): 
        success = asset_renamer_tools.rename_asset_func( old_path, new_path, True)
        
        states.end_process_log.append(
            f"{'renamed' if success else 'Error: Failed renaming'}: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")

        ui_progress_bar.update_progress_bar(len(self.assets_listbox.get_selected_items()))

    def extract_unused_assets_func(self):
        """
        will check if assets are used in any level, weapon, particle, or other game files. 
        If asset is not used anywhere, files will be moved in "unused assets" folder
        """

        if self.assets_listbox.get_selected_items() is None:
            states.notice_label.set_text("Select assets first", color="red")
            return
             
        
        GT.start_process("extract unused assets")
        
        extracted_assets =  extract_assets_tools.extract_unused_assets(self.assets_listbox.get_selected_items())

#        Créer un dictionnaire avec les anciens chemins relatifs et les nouveaux chemins
        formatted_log_entry = {
            os.path.relpath(extracted_asset, states.root_path): (os.path.relpath(extracted_asset, states.root_path)).replace("Assets", "Unused Assets")
            for extracted_asset in extracted_assets
        }

        # Générer les messages de log pour impression
        states.end_process_log = "no file extracted" if extracted_assets == [] else "\n".join( [
            f"Moved {old_path} -> {new_path}"
            for old_path, new_path in formatted_log_entry.items()
        ])
        
        GT.end_process("extract unused assets", states.end_process_log)
        self.page_update_items()

    def check_name_coherence(self):
        """
        Will cehck if assetname, parent name, etc, are coherent inside all files.
        Also will remove spaces and double. 
        """
        if self.assets_listbox.get_selected_items() is None:
            states.notice_label.set_text("Select assets first", color="red")
            return

        GT.start_process("Check cohrence in files")
        
        #Well, no details about the log here, would be too much work, main info are already in the log anyway 
        
        log_selected_items_lenght = len(self.assets_listbox.get_selected_items())

        for asset_path in self.assets_listbox.get_selected_items():
            # Check if the asset has a space in its name
            asset_renamer_tools.rename_asset_func( asset_path, asset_path, True, check_cohrence_mode=True)

            ui_progress_bar.update_progress_bar(log_selected_items_lenght)

        # Refresh the listbox after processing
        self.assets_listbox.update_items(GT.get_all_assets())

        GT.end_process("Check cohrence in files", "this func can't record which files have been affected, see previous logs in console", True)
