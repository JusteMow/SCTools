# 📝 Changelog - SCTools

## 2025-11-03

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

