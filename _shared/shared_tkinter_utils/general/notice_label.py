"""
📦 NoticeLabel - Label de notification stylisé

🔧 COMPOSANTS :
- Frame container
- Label avec texte et couleur personnalisables

📋 VARIABLES PRINCIPALES :
- self.label : widget Label tkinter
- self.frame : Frame container

🎯 USAGE BASIQUE :
    notice = NoticeLabel(parent)
    notice.pack(side="right", fill="x", pady=5)
    
    # Mettre à jour le texte et la couleur
    notice.set_text("Operation successful!", color="green")
    notice.set_text("Error occurred", color="red")
    notice.set_text("Warning", color="yellow")

💡 MÉTHODES PUBLIQUES :
- set_text(text, color="yellow") : change texte et couleur
- pack(**kwargs) / grid(**kwargs) : placement du widget

🎨 COULEURS RECOMMANDÉES :
- "yellow" : informations générales
- "green" : succès
- "red" : erreurs
- "orange" : avertissements
- "white" : neutre
"""

import tkinter as tk

class NoticeLabel(): 
    def __init__(self, parent, initial_text="Welcome !", initial_color="yellow"):
        """
        Initializes a notice label widget.
        
        Args:
            parent (tk.Widget): Parent widget
            initial_text (str): Initial text to display
            initial_color (str): Initial text color
        """
        # Frame container
        self.frame = tk.Frame(parent, bg="#2E2E2E", width=200)
        
        # Label widget
        self.label = tk.Label(
            self.frame, 
            text=initial_text, 
            bg="#2E2E2E", 
            fg=initial_color, 
            font=("Arial", 10)
        )
        self.label.pack(pady=5, side="right")

    def set_text(self, text, color="yellow"):
        """
        Updates the notice label text and color.
        
        Args:
            text (str): New text to display
            color (str): New text color (default: yellow)
        """
        self.label.config(text=text, fg=color)
        self.label.update_idletasks()
    
    def pack(self, **kwargs):
        """Packs the frame into the parent."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grids the frame into the parent."""
        self.frame.grid(**kwargs)

