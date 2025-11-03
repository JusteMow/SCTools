# 🛠️ SCTools

Outils de gestion d'assets pour **Shmup Creator** (BuloStudio).

## 📦 Installation

### 1. Cloner le repo avec submodules

```bash
git clone --recurse-submodules https://github.com/JusteMow/SCTools.git
cd SCTools
```

Ou si déjà cloné sans submodules :

```bash
git submodule update --init --recursive
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
pip install -e _shared/tkshared
```

### 3. Lancer l'application

```bash
python main.py
```

Ou via le batch :

```bash
Run_Asset_Renamer.bat
```

---

## 🎯 Fonctionnalités

- **Rename Assets** : Renommer sprites, sons, etc. dans gamebox et levels
- **Swap Enemies** : Échanger 2 enemies dans tous les levels
- **Set Enemy Props** : Modifier propriétés d'ennemis en masse
- **Clone Enemy** : Cloner un enemy dans gamebox.waves
- **Clone Level** : Cloner un level avec nouveau nom
- **Rename Levels** : Renommer levels et leurs screenNames
- **Show Info** : Afficher infos sur particules et autres assets

---

## 📚 Documentation

Voir [doc_main.md](doc_main.md) pour architecture et détails techniques.

---

## 🔧 Développement

### Mettre à jour le submodule tkshared

```bash
cd _shared/tkshared
git pull origin main
cd ../..
git add _shared/tkshared
git commit -m "Update tkshared submodule"
```

### Modifier le package partagé

Les modifications dans `_shared/tkshared/` doivent être commitées et pushées dans le repo [tk_shared](https://github.com/JusteMow/tk_shared).

---

## 🐛 Dépendances

- Python 3.8+
- tkinter (inclus dans Python)
- lxml
- Pillow
- [tkshared](https://github.com/JusteMow/tk_shared) (via submodule)

---

## 📝 Changelog

Voir [changelog.md](changelog.md) pour historique des modifications.

