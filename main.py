import os
import sys
import tkinter as tk
from tkinter import filedialog
from pages.rename_assets_page import RenameAssetsPage
from pages.swap_enemies_page import SwapEnemiesPage
from pages.set_enemy_props_page import SetEnemyPropsPage
from pages.clone_enemy_page import CloneEnemyPage
from pages.clone_level_page import CloneLevelPage
from pages.rename_levels_pages import RenameLevelsPage
from pages.show_info_page import ShowInfosPage
import states.states as states
import utils.log_file as log
from _shared.shared_tkinter_utils.general.notice_label import NoticeLabel


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Asset Manager")
        self.geometry("1000x800")
        self.configure(bg="#2E2E2E")

        # Attributs partagés
        self.current_page = None

        # Barre de navigation (haut partagé)
        self.setup_navigation()

        # Frame dynamique pour afficher les pages
        self.dynamic_frame = tk.Frame(self, bg="#2E2E2E")
        self.dynamic_frame.pack(fill="both", expand=True)

        # Charger la première page
        self.switch_page("rename")

    def setup_navigation(self):
        """
        Configure la barre de navigation avec les boutons de contrôle.
        """
        main_frame = tk.Frame(self, bg="#2E2E2E", height=80)
        main_frame.pack(fill="x", pady=5)

        # Barre supérieure
        top_frame = tk.Frame(main_frame, bg="#2E2E2E")
        top_frame.pack(fill="x", pady=5)
        

        # Reload App
        reload_button = tk.Button(top_frame, text="Reload App", command=self.reload_program,
                                  bg="#444", fg="white", relief="flat")
        reload_button.pack(side="left", padx=5)

        # Root directory label et bouton
        self.root_label = tk.Label(top_frame, text="Root Directory: None", bg="#2E2E2E", fg="white")
        self.root_label.pack(side="left", padx=5)

        select_root_button = tk.Button(top_frame, text="Select Root Directory", command=self.select_root_directory,
                                       bg="#444", fg="white", relief="flat")
        select_root_button.pack(side="left", padx=5)

        # Title
        title_label = tk.Label(top_frame, text="SC Tools by Juste Mow", bg="#2E2E2E", fg="white", font=("Arial", 16))
        title_label.pack(side="right", padx=5)


        menu_frame = tk.Frame(main_frame, bg="#2E2E2E")
        menu_frame.pack(fill = "x")       

        # !: Créer et stocker instance globale NoticeLabel pour feedback utilisateur
        states.notice_label = NoticeLabel(menu_frame, initial_text="Welcome ! Select root path")
        states.notice_label.pack(fill="x", pady=5, side="right")

        self.debug_mode_var = tk.BooleanVar(value=states.debug_mode)
        tk.Checkbutton(
                menu_frame, text="Debug", variable=self.debug_mode_var,
                command=self.set_debug_mode, bg="#2E2E2E", fg="white", selectcolor="#444"
            ).pack( side= "left", padx=10)

        # Navigation boutons
        navigation_frame = tk.Frame(menu_frame, bg="#2E2E2E")
        navigation_frame.pack(padx=5)

        tk.Button(navigation_frame, text="Rename Assets", command=lambda: self.switch_page("rename"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5)

        tk.Button(navigation_frame, text="Swap Enemies", command=lambda: self.switch_page("swap"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5)

        tk.Button(navigation_frame, text="Set Enemy Props", command=lambda: self.switch_page("enemy_props"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5)
        
        tk.Button(navigation_frame, text="Clone Enemies", command=lambda: self.switch_page("clone_enemy"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5)
        
        tk.Button(navigation_frame, text="Rename Levels", command=lambda: self.switch_page("rename_levels"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5) 
        
        tk.Button(navigation_frame, text="Clone Levels", command=lambda: self.switch_page("clone_levels"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5)
        
        tk.Button(navigation_frame, text="Show Particles Infos", command=lambda: self.switch_page("show_particles_info"),
                  bg="#444", fg="white", relief="flat").pack(side="left", padx=5)
        
        states.root_path = "C:\\Users\\MO\\\Documents\\BuloStudio\\Games\\Bullethell Lite"
        self.update_idletasks()

    def reload_program(self):
        """
        Recharge l'application en redémarrant le processus.
        """
        self.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def select_root_directory(self):
        """
        Ouvre une boîte de dialogue pour sélectionner le root directory.
        """
        root_path = filedialog.askdirectory()
        if root_path:
            states.root_path = root_path
            truncated_root_path = root_path if len(root_path) <= 50 else f"...{root_path[-50:]}"
            self.root_label.config(text=f"Root Directory: {truncated_root_path}")
            states.notice_label.set_text("Ready !", "yellow")
            if self.current_page:
                self.current_page.page_update_items()

    def switch_page(self, page_name):
        """
        Permet de basculer entre les pages dynamiques.
        """
        # Nettoyer la frame dynamique
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Charger la nouvelle page
        if page_name == "rename":
            self.current_page = RenameAssetsPage(self.dynamic_frame)
        elif page_name == "swap":
            self.current_page = SwapEnemiesPage(self.dynamic_frame)
        elif page_name == "enemy_props":
            self.current_page = SetEnemyPropsPage(self.dynamic_frame)
        elif page_name == "clone_enemy":
            self.current_page = CloneEnemyPage(self.dynamic_frame)
        elif page_name == "rename_levels":
            self.current_page = RenameLevelsPage(self.dynamic_frame)
        elif page_name == "clone_levels":
            self.current_page = CloneLevelPage(self.dynamic_frame)
        elif page_name == "show_particles_info":
            self.current_page = ShowInfosPage(self.dynamic_frame)
        

        # Afficher la nouvelle page
        if self.current_page:
            self.current_page.create_page().pack(fill="both", expand=True)
        
    def set_debug_mode(self): 
        states.debug_mode = self.debug_mode_var.get()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
