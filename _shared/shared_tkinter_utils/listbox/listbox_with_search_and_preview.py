"""
📦 ListboxWithSearchAndPreview - Listbox avec recherche + preview d'image

🔧 HÉRITE DE : ListboxWithSearch
AJOUTE : Canvas pour afficher preview d'image lors de sélection

📋 VARIABLES SUPPLÉMENTAIRES :
- self.preview_dir : dossier où chercher les images
- self.canvas : Canvas tkinter pour afficher l'image

🎯 USAGE BASIQUE :
    items = ["image1.png", "image2.jpg", "document.txt"]
    preview_dir = "C:/my_images/"
    
    lb = ListboxWithSearchAndPreview(
        parent, 
        items, 
        preview_dir, 
        "My Images",
        selectmode=tk.SINGLE
    )
    lb.pack(side="left", fill="both", expand=True)

💡 COMPORTEMENT :
- Au clic sur item, cherche image dans preview_dir
- Affiche l'image redimensionnée 150x150 dans canvas
- Si fichier non-image ou introuvable, canvas vide
- Formats supportés : .png, .jpg, .jpeg, .bmp, .psd, .pic, .gif, .tga, .ppm, .pgm, .hdr, .dds

🔄 USAGE AVANCÉ (HÉRITAGE) :
    
    class MyCustomPreviewListbox(ListboxWithSearchAndPreview):
        def __init__(self, parent, items, preview_dir):
            super().__init__(parent, items, preview_dir, "My Title")
        
        # Override pour modifier comportement preview
        def update_preview(self, item):
            # Custom logic : chercher dans plusieurs dossiers, transformer path, etc.
            custom_path = self.get_custom_image_path(item)
            try:
                image = Image.open(custom_path).resize((150, 150), Image.Resampling.LANCZOS)
                image_tk = ImageTk.PhotoImage(image)
                self.canvas.delete("all")
                self.canvas.create_image(75, 75, image=image_tk)
                self.canvas.image = image_tk  # !: Keep reference to avoid garbage collection
            except Exception as e:
                print(f"Error: {e}")
                self.canvas.delete("all")

⚠️ IMPORTANT :
- Nécessite PIL/Pillow : pip install Pillow
- Garder référence à image_tk (self.canvas.image = image_tk) pour éviter garbage collection
- update_preview() est appelé automatiquement dans on_select()

💡 MÉTHODES OVERRIDABLES :
- update_preview(item) : custom logic pour afficher preview
- on_select(event) : override pour ajouter actions après sélection
"""

import os
import tkinter as tk
from PIL import Image, ImageTk
from _shared.shared_tkinter_utils.listbox.listbox_with_search import ListboxWithSearch

class ListboxWithSearchAndPreview(ListboxWithSearch):
    def __init__(self, parent, items, preview_dir, title, selectmode=tk.SINGLE, on_select_callback=None):
        """
        Initializes a searchable listbox with a title, scrollbar, and image preview.

        Args:
            parent (tk.Widget): Parent widget (frame or root).
            items (list): List of items to populate the listbox.
            preview_dir (str): Directory to search for images.
            title (str): Title displayed above the listbox.
            selectmode (tk.SelectMode): SINGLE or MULTIPLE selection mode.
            on_select_callback (function): Callback triggered on selection.
        """
        super().__init__(parent, items, title, selectmode, on_select_callback)
        self.preview_dir = preview_dir

        # Preview canvas
        self.canvas = tk.Canvas(self.frame, width=150, height=150, bg="#1E1E1E", relief="flat")
        self.canvas.pack(pady=5)

    def update_preview(self, item):
        """
        Updates the preview canvas with the image associated with the selected item.

        Args:
            item (str): Selected item name.
        """
        try:
            image_path = os.path.join(self.preview_dir, item)
            if not os.path.exists(image_path):
                self.canvas.delete("all")
                return

            if os.path.splitext(image_path)[1] in [".png", ".jpg", ".jpeg", ".bmp", ".psd", ".pic", ".gif", ".tga", "ppm", ".pgm", ".hdr", ".dds"] :

                # Load and resize image
                image = Image.open(image_path).resize((150, 150), Image.Resampling.LANCZOS)
                image_tk = ImageTk.PhotoImage(image)

                # Update canvas
                self.canvas.delete("all")
                self.canvas.create_image(75, 75, image=image_tk)
                self.canvas.image = image_tk  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error loading preview for {item}: {e}")
            self.canvas.delete("all")

    def on_select(self, event):
        """
        Handles item selection and updates the preview image.
        """
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        selected_item = self.filtered_items[selected_index[0]]
        self.update_preview(selected_item)

        super().on_select(event)

