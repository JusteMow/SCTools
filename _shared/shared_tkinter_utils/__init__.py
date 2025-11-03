"""
📦 shared_tkinter_utils - Widgets tkinter réutilisables

🎯 USAGE RAPIDE :

# Imports individuels
from _shared.shared_tkinter_utils.general.entry_plus import EntryPlus
from _shared.shared_tkinter_utils.general.notice_label import NoticeLabel
from _shared.shared_tkinter_utils.general.screen_name_filter import ScreenNameFilter
from _shared.shared_tkinter_utils.listbox.listbox_with_search import ListboxWithSearch
from _shared.shared_tkinter_utils.listbox.listbox_with_search_and_preview import ListboxWithSearchAndPreview

# Ou imports simplifiés
from _shared.shared_tkinter_utils import general, listbox

entry = general.entry_plus.EntryPlus(parent, validation_type="integer")
lb = listbox.listbox_with_search.ListboxWithSearch(parent, items, "Title")
"""

# Import des sous-modules pour faciliter l'accès
from _shared.shared_tkinter_utils import general
from _shared.shared_tkinter_utils import listbox

__all__ = ['general', 'listbox']

