# 📋 SCTools - Documentation Principale

Outils de gestion d'assets pour StarChild (BuloStudio).

---

## 🏗️ ARCHITECTURE

```
SCTools/
├── main.py                 # Entry point, navigation entre pages
├── pages/                  # Pages de l'interface (7 pages)
├── utils/                  # Outils de traitement XML, assets, levels
│   └── ui_utils/          # Widgets UI spécifiques au projet
├── states/                 # Variables globales d'état
├── _shared/               # 📦 Package réutilisable (nouveau)
│   └── shared_tkinter_utils/
└── old/                   # Anciens fichiers (backup)
```

---

## 📦 PAGES PRINCIPALES

### 1. **rename_assets_page.py**
Renomme assets (sprites, sons, etc.) dans gamebox et levels

### 2. **swap_enemies_page.py**
Échange 2 enemies dans tous les levels

### 3. **set_enemy_props_page.py**
Modifie propriétés d'ennemis en masse

### 4. **clone_enemy_page.py**
Clone un enemy dans gamebox.waves

### 5. **clone_level_page.py**
Clone un level avec nouveau nom

### 6. **rename_levels_pages.py**
Renomme levels et leurs screenNames

### 7. **show_info_page.py**
Affiche infos sur particules et autres assets

---

## 🛠️ UTILS PRINCIPAUX

### **asset_renamer_tools.py**
Fonctions de renommage dans gamebox (backgrounds, enemies, items, players, weapons, etc.)

### **gamebox_tools.py**
Manipulation gamebox XML (lecture, écriture, validation)

### **levels_tools.py**
Manipulation levels XML (enemies, items, backgrounds, sons, etc.)

### **xml_tools.py**
Fonctions bas-niveau XML (lxml)

### **ui_utils/**
Widgets tkinter spécifiques au projet :
- `listbox_all_assets.py` : Listbox assets avec détection conflits/espaces
- `listbox_levels.py` : Listbox levels avec screenNames

---

## 📦 _shared/shared_tkinter_utils/ (NOUVEAU)

Package réutilisable extrait du projet. Voir `_shared/shared_tkinter_utils/README.md`

**Contenu** :
- `general/` : EntryPlus, NoticeLabel, ScreenNameFilter
- `listbox/` : ListboxWithSearch, ListboxWithSearchAndPreview

---

## 🔄 PIPELINE GÉNÉRAL

### Changement de root_path :
```
main.select_root_directory()
└─> states.root_path = new_path
    └─> current_page.page_update_items()
        └─> Reload listbox avec nouveaux items
```

### Traitement rename_asset (exemple) :
```
rename_assets_page.rename_button_click()
├─> asset_renamer_tools.rename_asset(old_name, new_name)
│   ├─> rename_asset_in_gamebox_xxx() selon type d'asset
│   └─> rename_asset_in_level_xxx() pour chaque level
├─> log_file.log_entry() pour traçabilité
└─> NoticeLabel.set_notiche_label() pour feedback
```

---

## 🌐 STATES GLOBAUX (states/states.py)

- `root_path` : Chemin racine du projet StarChild
- `found_error` : Erreur détectée pendant traitement
- `found_warning` : Warning détecté
- `debug_mode` : Mode debug (logs verbeux)
- `progress_bar` : Progression actuelle
- `opened_gamebox` : Gamebox actuellement ouvert

---

## 🎨 UI/UX

- **Thème** : Dark (#2E2E2E bg, #1E1E1E widgets)
- **Navigation** : Boutons top-bar pour switch entre pages
- **Feedback** : NoticeLabel (jaune=info, vert=succès, rouge=erreur)
- **Debug** : Checkbox pour activer logs verbeux

---

## 🔧 NOTES TECHNIQUES

### XML Structure
- Gamebox : `(root)/gamebox/gamebox.xxx`
- Levels : `(root)/levels/LevelXXX.level`
- Assets : `(root)/Assets/`

### Dépendances
- `tkinter` (GUI)
- `lxml` (XML parsing)
- `PIL/Pillow` (images preview, optionnel)

### Conventions
- Pas de style/script inline
- Margins bannis (Flex uniquement)
- Try/except pour robustesse
- Logs pour traçabilité

---

## 📝 TODO / AMÉLIORATIONS

- [ ] Ajouter doc en en-tête des fichiers utils/ et pages/
- [ ] Migrer NoticeLabel vers version refactorisée (_shared)
- [ ] Réorganiser dossiers utils/ (trop de fichiers à la racine)
- [ ] Tests unitaires pour fonctions critiques

