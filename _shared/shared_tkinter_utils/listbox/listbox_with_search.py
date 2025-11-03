"""
📦 ListboxWithSearch - Listbox tkinter avec recherche et sélection multiple

🔧 COMPOSANTS :
- Title label
- Barre de recherche (Entry auto-filtrée)
- Listbox avec scrollbar
- Checkbox "Select All" (si selectmode MULTIPLE/EXTENDED)

📋 VARIABLES IMPORTANTES (accessibles pour héritage) :
- self.items : liste complète des items
- self.filtered_items : liste filtrée selon search_var
- self.search_var : StringVar de la barre de recherche
- self.listbox : widget Listbox tkinter
- self.frame : Frame principal contenant tous les widgets
- self.on_select_callback : callback appelé lors de sélection

🎯 USAGE BASIQUE :
    items = ["item1", "item2", "item3"]
    lb = ListboxWithSearch(parent, items, "My Title", selectmode=tk.SINGLE)
    lb.pack(side="left", fill="both", expand=True)
    
    selected = lb.get_selected_item()  # Pour SINGLE
    selected = lb.get_selected_items()  # Pour MULTIPLE (retourne liste ou None)

🔄 USAGE AVANCÉ (HÉRITAGE) :
    
    class MyCustomListbox(ListboxWithSearch):
        def __init__(self, parent, items, title):
            super().__init__(parent, items, title, selectmode=tk.MULTIPLE)
        
        # Override pour filtrage custom
        def filter_items(self, *args):
            search_term = self.search_var.get().lower()
            self.filtered_items = [item for item in self.items if my_custom_filter(item, search_term)]
        
        # Override pour affichage custom (colorisation, formatage)
        def private_update_listbox(self, *args):
            self.filter_items()
            self.listbox.delete(0, tk.END)
            for item in self.filtered_items:
                self.listbox.insert(tk.END, format_item(item))
                if is_special(item):
                    self.listbox.itemconfig(tk.END, {"bg": "yellow", "fg": "black"})
        
        # Override pour format de retour custom
        def get_selected_items(self):
            indices = self.listbox.curselection()
            return [custom_format(self.filtered_items[i]) for i in indices]

🔄 CALLBACKS :
    def my_callback(selected_items):
        print(f"Selected: {selected_items}")
    
    lb = ListboxWithSearch(parent, items, "Title", on_select_callback=my_callback)

💡 MÉTHODES PUBLIQUES :
- update_items(items) : recharge les items (garde sélection si possible)
- get_selected_items() : retourne liste d'items sélectionnés ou None
- get_selected_item() : retourne 1er item sélectionné ou None
- pack(**kwargs) / grid(**kwargs) : placement du widget
"""

import tkinter as tk

class ListboxWithSearch:
    def __init__(self, parent, items, title, selectmode=tk.SINGLE, on_select_callback=None):
        """
        Initializes a searchable listbox with a title and scrollbar.

        Args:
            parent (tk.Widget): Parent widget (frame or root).
            items (list): List of items to populate the listbox.
            title (str): Title displayed above the listbox.
            selectmode (tk.SelectMode): SINGLE or MULTIPLE selection mode.
            on_select_callback (function): Callback triggered on selection.
        """
        self.parent = parent
        self.items = items
        self.title = title
        self.selectmode = selectmode
        self.selected_index = None
        self.on_select_callback = on_select_callback

        self.frame = tk.Frame(self.parent, bg="#2E2E2E")

        # Title
        self.title_label = tk.Label(self.frame, text=self.title, bg="#2E2E2E", fg="white", font=("Arial", 12))
        self.title_label.pack(pady=(5, 0))

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.frame, textvariable=self.search_var, bg="#1E1E1E", fg="white",
                                     insertbackground="white", relief="flat", width=30)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_var.trace_add("write", self.private_update_listbox)

        # Listbox and scrollbar
        listbox_frame = tk.Frame(self.frame, bg="#2E2E2E")
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(listbox_frame, width=30, height=15, bg="#1E1E1E", fg="white",
                                  selectbackground="#444", selectforeground="white", relief="flat",
                                  exportselection=False, selectmode=self.selectmode)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.scrollbar = tk.Scrollbar(listbox_frame, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.update_items(items)


        if selectmode == tk.MULTIPLE or selectmode == tk.EXTENDED :
            # Select all Button
            self.select_all_var = tk.BooleanVar(value=False)
            self.select_all_checkbox = tk.Checkbutton(
                self.frame,
                text="Select All",
                variable=self.select_all_var,
                bg="#2E2E2E",
                fg="white",
                selectcolor="#444",
                command=self.select_all
            )
            self.select_all_checkbox.pack(pady=5)  # Place it below the listbox

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def update_items(self, items):
        """
        Mainly a callback function called on root path select.
        Updates the listbox and retains the previous selection if possible.
        """
        self.items = items
        selected_indices = self.listbox.curselection()  # Stocker les indices sélectionnés
        self.private_update_listbox()  # Mettre à jour la liste

        # Réappliquer les sélections valides
        for index in selected_indices:
            if index < len(self.items):  # Vérifier que l'indice est toujours valide
                self.listbox.select_set(index)

    
    #filter with search bar, *args because of call by entry field
    def private_update_listbox(self, *args):
        """
        Updates the listbox with the current filtered items.
        """
        self.filter_items()
        
        self.listbox.delete(0, tk.END)
        for item in self.filtered_items:
            self.listbox.insert(tk.END, item)

    def filter_items(self, *args):
        """
        Filters the listbox items based on the search term.
        """
        search_term = self.search_var.get().lower()
        self.filtered_items = [item for item in self.items if search_term in item.lower()]


    def get_selected_items(self):
        """
        Returns the LIST of selected items.
        Will return None if nothing selected
        """
        selected_indices = self.listbox.curselection()
        return None if not selected_indices else [self.filtered_items[i] for i in selected_indices]
    
    def get_selected_item(self):
        """
        Returns the LIST of selected items.
        Will return None if nothing selected
        """
        selected_indices = self.listbox.curselection()
        return None if not selected_indices else [self.filtered_items[i] for i in selected_indices][0]
    
    def on_select(self, event):
        """
        Handles item selection and updates the preview image.
        """
        if self.on_select_callback:
            selected_items = self.get_selected_items()  # Récupère les éléments sélectionnés
            self.on_select_callback(selected_items) 
    
    def select_all(self):
        """
        Select or deselect all levels in the levels listbox.
        """
        if self.select_all_var.get():
            self.listbox.select_set(0, tk.END)
        else:
            self.listbox.selection_clear(0, tk.END)

