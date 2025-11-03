"""
📦 ScreenNameFilter - Widget de filtrage Include/Exclude

🔧 COMPOSANTS :
- 2 Entry fields : Include et Exclude
- Labels explicatifs
- Callbacks optionnels sur changement

📋 VARIABLES PRINCIPALES :
- self.include_var : StringVar pour filtre include
- self.exclude_var : StringVar pour filtre exclude
- self.frame : Frame principal

🎯 USAGE BASIQUE :
    def on_include(value):
        print(f"Include filter: {value}")
    
    def on_exclude(value):
        print(f"Exclude filter: {value}")
    
    filter_widget = ScreenNameFilter(
        parent, 
        include_callback=on_include,
        exclude_callback=on_exclude
    )
    filter_widget.pack(side="top", fill="x")
    
    # Vérifier si item passe le filtre
    if filter_widget.match_filter("my_item_name"):
        print("Item passes filter")

💡 MÉTHODES PUBLIQUES :
- match_filter(screenName) : retourne True si item passe les filtres, False sinon
- get_include_filter() : retourne valeur du filtre include
- get_exclude_filter() : retourne valeur du filtre exclude

🔄 LOGIQUE DE FILTRAGE :
- Si include_filter non vide : item DOIT contenir include_filter
- Si exclude_filter non vide : item NE DOIT PAS contenir exclude_filter
- Si les 2 : item doit satisfaire les 2 conditions
- Si les 2 vides : tous les items passent
"""

import tkinter as tk


class ScreenNameFilter:
    def __init__(self, parent, include_callback=None, exclude_callback=None):
        """
        Initializes the ScreenNameFilter widget.

        Args:
            parent (tk.Frame): Parent widget where the filter will be placed.
            include_callback (function): Optional callback function for include filter changes.
            exclude_callback (function): Optional callback function for exclude filter changes.
        """
        self.parent = parent
        self.include_callback = include_callback
        self.exclude_callback = exclude_callback

        # Main Frame
        self.frame = tk.Frame(self.parent, bg="#2E2E2E")

        # Labels and Entries for Include Filter
        self.filter_label = tk.Label(self.frame, text="Filter by Name:", bg="#2E2E2E", fg="white", font=("Arial", 10))
        self.filter_label.pack(anchor="center", pady=(5, 0))

        self.filter_label2 = tk.Label(self.frame, text="Only if screenName contains", bg="#2E2E2E", fg="white", font=("Arial", 10))
        self.filter_label2.pack(anchor="center", pady=(2, 0))

        self.include_var = tk.StringVar()
        self.filter_include_entry = tk.Entry(self.frame, textvariable=self.include_var, bg="#1E1E1E", fg="white",
                                             relief="flat", insertbackground="white", width=20)
        self.filter_include_entry.pack(pady=(0, 5))
        self.include_var.trace_add("write", lambda *args: self.on_include_change())

        # Labels and Entries for Exclude Filter
        self.filter_label3 = tk.Label(self.frame, text="Exclude if screenName contains", bg="#2E2E2E", fg="white", font=("Arial", 10))
        self.filter_label3.pack(anchor="center", pady=(2, 0))

        self.exclude_var = tk.StringVar()
        self.filter_exclude_entry = tk.Entry(self.frame, textvariable=self.exclude_var, bg="#1E1E1E", fg="white",
                                             relief="flat", insertbackground="white", width=20)
        self.filter_exclude_entry.pack(pady=(0, 5))
        self.exclude_var.trace_add("write", lambda *args: self.on_exclude_change())

        # Info Label
        self.filter_label4 = tk.Label(self.frame, text="Ignored if empty", bg="#2E2E2E", fg="white", font=("Arial", 10))
        self.filter_label4.pack(anchor="center", pady=(2, 0))

    def pack(self, **kwargs):
        """
        Packs the filter frame into the parent.
        """
        self.frame.pack(**kwargs)

        #if screenName contains spme tag that you set to filter
    def match_filter(self, screenName):
        """
        Applies include/exclude filters based on screenName.
        Returns False if the enemy should be skipped, True otherwise.
        """
        if not screenName:  # Handle missing or empty screenName
            return True
 
        #if screenName contains spme tag that you set to filter
        include_filter = self.filter_include_entry.get().strip()  # Get the include filter
        exclude_filter = self.filter_exclude_entry.get().strip()  # Get the exclude filter

        if include_filter and include_filter not in screenName:  # Include filter
            return False
        if exclude_filter and exclude_filter in screenName:  # Exclude filter
            return False

        return True

    def get_include_filter(self):
        """
        Returns the value of the include filter.
        """
        return self.include_var.get().strip()

    def get_exclude_filter(self):
        """
        Returns the value of the exclude filter.
        """
        return self.exclude_var.get().strip()

    def on_include_change(self):
        """
        Callback for include filter changes.
        """
        if self.include_callback:
            self.include_callback(self.get_include_filter())

    def on_exclude_change(self):
        """
        Callback for exclude filter changes.
        """
        if self.exclude_callback:
            self.exclude_callback(self.get_exclude_filter())

