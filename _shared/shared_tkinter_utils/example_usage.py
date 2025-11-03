"""
Exemple d'utilisation des widgets shared_tkinter_utils
"""

import tkinter as tk
from _shared.shared_tkinter_utils.general import EntryPlus, NoticeLabel, ScreenNameFilter
from _shared.shared_tkinter_utils.listbox import ListboxWithSearch, ListboxWithSearchAndPreview

def create_example_window():
    """
    Crée une fenêtre d'exemple avec tous les widgets
    """
    root = tk.Tk()
    root.title("shared_tkinter_utils - Example")
    root.geometry("800x600")
    root.configure(bg="#2E2E2E")
    
    # Frame gauche pour les entries et filters
    left_frame = tk.Frame(root, bg="#2E2E2E")
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # Frame droite pour les listbox
    right_frame = tk.Frame(root, bg="#2E2E2E")
    right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # Notice Label en haut
    notice = NoticeLabel(root, initial_text="Bienvenue ! Teste les widgets ci-dessous")
    notice.pack(side="top", fill="x", pady=5)
    
    # === LEFT FRAME : Entries et Filters ===
    
    # Title
    tk.Label(left_frame, text="EntryPlus Examples", bg="#2E2E2E", fg="white", 
             font=("Arial", 14, "bold")).pack(pady=(0, 10))
    
    # EntryPlus - Integer
    tk.Label(left_frame, text="Positive Integer:", bg="#2E2E2E", fg="white").pack()
    entry_int = EntryPlus(left_frame, validation_type="positive_integer", width=20)
    entry_int.pack(pady=(0, 10))
    
    # EntryPlus - Float 0-1
    tk.Label(left_frame, text="Float (0-1):", bg="#2E2E2E", fg="white").pack()
    entry_float = EntryPlus(left_frame, validation_type="float_0_1", width=20)
    entry_float.pack(pady=(0, 10))
    
    # EntryPlus - Name
    tk.Label(left_frame, text="Name (alphanumeric):", bg="#2E2E2E", fg="white").pack()
    entry_name = EntryPlus(left_frame, validation_type="name", width=20)
    entry_name.pack(pady=(0, 20))
    
    # ScreenNameFilter
    def on_filter_change(value):
        notice.set_text(f"Filter changed: {value}", color="cyan")
    
    filter_widget = ScreenNameFilter(
        left_frame,
        include_callback=lambda v: on_filter_change(f"Include: {v}"),
        exclude_callback=lambda v: on_filter_change(f"Exclude: {v}")
    )
    filter_widget.pack(pady=10)
    
    # Button pour tester les valeurs
    def show_values():
        values = f"Int: {entry_int.get()}, Float: {entry_float.get()}, Name: {entry_name.get()}"
        notice.set_text(values, color="green")
    
    tk.Button(left_frame, text="Show Entry Values", command=show_values,
              bg="#444", fg="white").pack(pady=10)
    
    # === RIGHT FRAME : Listbox ===
    
    # ListboxWithSearch
    items = [f"Item {i}" for i in range(1, 51)]
    
    def on_select(selected_items):
        if selected_items:
            notice.set_text(f"Selected: {selected_items}", color="yellow")
    
    listbox = ListboxWithSearch(
        right_frame,
        items,
        "ListboxWithSearch",
        selectmode=tk.MULTIPLE,
        on_select_callback=on_select
    )
    listbox.pack(fill="both", expand=True, pady=(0, 10))
    
    # Button pour récupérer sélection
    def get_selection():
        selected = listbox.get_selected_items()
        if selected:
            notice.set_text(f"Tu as sélectionné : {', '.join(selected)}", color="green")
        else:
            notice.set_text("Aucune sélection", color="orange")
    
    tk.Button(right_frame, text="Get Selection", command=get_selection,
              bg="#444", fg="white").pack()
    
    root.mainloop()

if __name__ == "__main__":
    create_example_window()

