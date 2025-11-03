"""
📦 BasePage - Template abstrait pour pages de l'application

🎯 PATTERN : Template Method (ABC)
Définit structure commune des pages avec hooks personnalisables.

🔧 MÉTHODES ABSTRAITES (à implémenter) :
- create_page() : Construit et retourne le frame principal de la page
- page_update_items() : Callback appelé lors du changement de root_path

🔧 MÉTHODES UTILITAIRES (spécifiques projet) :
- get_enemy_data() : Liste assets enemies du projet
- get_items_data() : Liste assets items du projet
- get_levels_data() : Liste fichiers .level du projet

🔄 PIPELINE D'USAGE :

1. Créer page (main.py) :
   page = MyCustomPage(parent_frame)
   page.create_page().pack(fill="both", expand=True)

2. Update root_path :
   main.select_root_directory()
   └─> states.root_path = new_path
       └─> current_page.page_update_items()
           └─> Reload listbox/data

📝 EXEMPLE D'IMPLÉMENTATION :

class MyCustomPage(BasePage):
    def create_page(self):
        frame = tk.Frame(self.root, bg="#2E2E2E")
        # Build UI...
        return frame
    
    def page_update_items(self):
        if states.root_path:
            items = self.get_enemy_data()
            self.listbox.update_items(items)

💡 PAGES EXISTANTES UTILISANT CE PATTERN :
- RenameAssetsPage, SwapEnemiesPage, SetEnemyPropsPage
- CloneEnemyPage, CloneLevelPage, RenameLevelsPage
"""

from abc import ABC, abstractmethod
import os
import tkinter as tk
import states.states as states


class BasePage(ABC):
    def __init__(self, root):
        self.root = root
        self.page = None  # Container for the page's widgets

    @abstractmethod
    def create_page(self):
        """
        Creates and populates the page. This method must return the page's main frame.
        """
        pass

    @abstractmethod
    def page_update_items(self):
        """
        Méthode abstraite pour recharger la page avec un nouveau root_dir.
        """
        pass

    def get_enemy_data(self):
        """
        Retrieve enemy asset names from the Assets directory.
        """
        enemies_path = os.path.join(states.root_path, "Assets", "Models", "Enemies")
        data = []
        if os.path.exists(enemies_path):
            for root, _, files in os.walk(enemies_path):
                for file in files:
                    data.append(os.path.basename(file))
        return data
    
    def get_items_data(self):
        """
        Retrieve enemy asset names from the Assets directory.
        """
        items_path = os.path.join(states.root_path, "Assets", "Models", "Items")
        data = []
        if os.path.exists(items_path):
            for root, _, files in os.walk(items_path):
                for file in files:
                    data.append(os.path.basename(file))
        return data

    def get_levels_data(self):
        """
        Retrieve level files with titles.
        """
        levels_path = os.path.join(states.root_path, "levels")
        data = []
        if os.path.exists(levels_path):
            for file in os.listdir(levels_path):
                if file.endswith(".level") and os.path.isfile(os.path.join(levels_path, file)):
                    data.append(file)
        return data