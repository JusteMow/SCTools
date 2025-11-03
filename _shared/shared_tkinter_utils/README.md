# 📦 shared_tkinter_utils

Widgets tkinter réutilisables pour créer des interfaces graphiques rapidement.

## 🎯 Contenu

### 📁 general/
- **EntryPlus** : Entry avec validation automatique (integer, float, name, etc.)
- **NoticeLabel** : Label de notification avec couleur customisable
- **ScreenNameFilter** : Widget include/exclude filter

### 📁 listbox/
- **ListboxWithSearch** : Listbox avec barre de recherche et select all
- **ListboxWithSearchAndPreview** : Listbox avec recherche + preview d'images

## 🚀 Installation

Aucune installation nécessaire. Copier le dossier `_shared/` dans votre projet.

**Dépendances** :
- Python 3.x
- tkinter (inclus dans Python standard)
- Pillow/PIL (uniquement pour `ListboxWithSearchAndPreview`) : `pip install Pillow`

## 💡 Usage rapide

```python
import tkinter as tk
from _shared.shared_tkinter_utils.general import EntryPlus, NoticeLabel
from _shared.shared_tkinter_utils.listbox import ListboxWithSearch

root = tk.Tk()

# Entry avec validation
entry = EntryPlus(root, validation_type="positive_integer")
entry.pack()

# Listbox avec recherche
items = ["item1", "item2", "item3"]
lb = ListboxWithSearch(root, items, "My List", selectmode=tk.SINGLE)
lb.pack(fill="both", expand=True)

# Notice label
notice = NoticeLabel(root)
notice.pack(side="bottom")
notice.set_text("Ready!", color="green")

root.mainloop()
```

## 📚 Documentation complète

Chaque fichier contient une documentation détaillée en en-tête avec :
- 🔧 Composants et fonctionnalités
- 📋 Variables importantes
- 🎯 Usage basique
- 🔄 Usage avancé (héritage)
- 💡 Méthodes et callbacks

Ouvrir les fichiers `.py` pour voir la doc complète.

## 🔄 Héritage et customisation

Tous les widgets sont conçus pour être facilement extensibles par héritage.

**Exemple** : Customiser ListboxWithSearch

```python
from _shared.shared_tkinter_utils.listbox import ListboxWithSearch
import tkinter as tk

class MyCustomListbox(ListboxWithSearch):
    def filter_items(self, *args):
        # Custom filtering logic
        search_term = self.search_var.get().lower()
        self.filtered_items = [
            item for item in self.items 
            if my_custom_condition(item, search_term)
        ]
    
    def private_update_listbox(self, *args):
        # Custom display logic
        self.filter_items()
        self.listbox.delete(0, tk.END)
        for item in self.filtered_items:
            self.listbox.insert(tk.END, format_item(item))
            if is_special(item):
                self.listbox.itemconfig(tk.END, {"bg": "yellow"})
```

## 📝 Changelog

Voir `changelog.md` pour historique des modifications.

