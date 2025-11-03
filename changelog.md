# 📝 Changelog - SCTools

## 2025-11-03 - Migration vers package Git partagé

### 🛠️ Scripts batch Git
- **git_push.bat** : Push automatique SCTools + submodule tkshared
- **git_pull.bat** : Pull et mise à jour du submodule tkshared

### 🎯 Migration tkshared (submodule Git)
- **Création repo GitHub** `TkinterSharedUI` (https://github.com/JusteMow/tk_shared)
  - Package renommé : `shared_tkinter_utils` → `tkshared`
  - Structure setup.py pour installation pip
  - Intégré comme submodule Git dans `_shared/tkshared`
- **Mise à jour imports** dans tout le projet
  - `from _shared.shared_tkinter_utils.xxx` → `from tkshared.xxx`
  - 11 fichiers mis à jour (pages, utils, main)
- **Suppression ancien dossier** `_shared/shared_tkinter_utils/`
  - Remplacé par submodule Git
  - Installation : `pip install -e _shared/tkshared`

### ✅ Création package réutilisable
- **Package** `_shared/shared_tkinter_utils/`
  - Extraction widgets réutilisables : EntryPlus, ListboxWithSearch, ListboxWithSearchAndPreview, NoticeLabel, ScreenNameFilter
  - Doc complète en en-tête de chaque fichier
  - README.md et changelog.md pour le package
  - example_usage.py pour démonstration

### 🔧 Migration vers nouveau package
- **Wrapper backward-compatibility** dans `utils/ui_utils/`
  - Anciens fichiers redirigent vers `_shared/` (DEPRECATED)
  - Pas de breaking changes pour code existant
- **Refactorisation NoticeLabel**
  - Suppression des globals (mauvaise pratique)
  - Instance globale dans `states.notice_label`
  - Nouvelle API : `.set_text(text, color)` au lieu de `.set_notiche_label()`
- **Mise à jour tous les appels**
  - main.py, pages/, utils/general_tools.py
  - Correction typo : "notiche" → "notice"
  - Correction typo : "not vali" → "not valid"

### 🧹 Nettoyage
- **Suppression fichiers proxy** dans `utils/ui_utils/`
  - entry_plus.py, screenName_filter.py, listbox_with_search.py, listbox_with_search_and_preview.py
  - Imports directs depuis `_shared/` maintenant
  - Plus clair pour maintenance future

### 📚 Documentation
- **Ajout** `doc_main.md` : documentation structure globale du projet
- **Ajout** `changelog.md` : journal des modifications du projet
- **Ajout** doc en-tête `pages/base_page.py` : explication pattern Template Method

