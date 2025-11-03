# 📝 Changelog - shared_tkinter_utils

## 2025-11-03 - Création du package

### ✅ Ajouté
- **Structure du package** `_shared/shared_tkinter_utils/`
  - Dossier `general/` pour widgets généraux
  - Dossier `listbox/` pour widgets listbox
  
- **general/entry_plus.py**
  - EntryPlus : Entry avec validation automatique
  - Types : integer, positive_integer, float, positive_float, float_0_1, name, format_xxx
  
- **general/notice_label.py**
  - NoticeLabel : Label de notification stylisé
  - Refactorisation : suppression des globals
  
- **general/screen_name_filter.py**
  - ScreenNameFilter : Widget include/exclude filter
  
- **listbox/listbox_with_search.py**
  - ListboxWithSearch : Listbox avec recherche et select all
  - Support SINGLE et MULTIPLE selectmode
  
- **listbox/listbox_with_search_and_preview.py**
  - ListboxWithSearchAndPreview : Listbox avec preview d'images
  - Canvas 150x150 pour affichage images
  
- **Documentation**
  - Doc complète en en-tête de chaque fichier
  - README.md avec exemples d'usage
  - __init__.py pour faciliter imports

### 🔧 Notes
- Package extrait de `utils/ui_utils/` du projet SCTools
- Éléments métier (`ListboxAllAssets`, `ListboxLevels`) conservés dans projet principal
- `progress_bar.py` non inclus (console, pas tkinter)

