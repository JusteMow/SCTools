"""
📦 EntryPlus - Entry tkinter avec validation automatique

🔧 FONCTIONS PRINCIPALES :
- EntryPlus(parent, validation_type, **kwargs) : Entry avec validation au focusout
- Validation automatique et correction des valeurs invalides

📋 TYPES DE VALIDATION DISPONIBLES :
- "integer" : entiers (positifs ou négatifs)
- "positive_integer" : entiers strictement positifs
- "float" : nombres décimaux
- "positive_float" : décimaux strictement positifs
- "float_0_1" : décimaux entre 0 et 1 (inclus)
- "name" : noms valides (alphanumériques, _, -, .)
- "format_xxx" : entiers positifs à 3 chiffres exactement

🎯 USAGE :
    entry = EntryPlus(parent, validation_type="positive_integer", width=10)
    entry.pack()
    value = entry.get()

💡 COMPORTEMENT :
- Validation déclenchée au focusout (quand on quitte le champ)
- Correction automatique si valeur invalide (pas d'erreur bloquante)
- Retourne "" si correction impossible

🔄 EXTENSION :
- Ajouter types dans validation_methods dict
- Implémenter _validate_xxx() et gérer dans get_corrected_value()
"""

import tkinter as tk

class EntryPlus(tk.Entry):

    def __init__(self, parent, validation_type=None, **kwargs):
        """
        Validate and correct the input value based on the validation type.
        Args: 
            validation_type (str): can be "integer", "positive_integer", "float", "positive_float", "float_0_1", "name"
        """
        super().__init__(parent, **kwargs)
        self.validation_type = validation_type

        # Mapping des fonctions de validation
        self.validation_methods = {
            "integer": self._validate_integer,
            "positive_integer": self._validate_positive_integer,
            "float": self._validate_float,
            "positive_float": self._validate_positive_float,
            "float_0_1": self._validate_float_0_1,
            "name": self._validate_name,
            "format_xxx": self._validate_format_xxx,  
        }

        if validation_type in self.validation_methods:
            self.validate_command = self.register(self._validate_and_correct)
            self.configure(validate="focusout", validatecommand=(self.validate_command, "%P"))

        self.valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")

    def _validate_and_correct(self, value):
        """
        Validate and correct the input value based on the validation type.
        """
        if self.validation_type in self.validation_methods:
            is_valid = self.validation_methods[self.validation_type](value)
            if not is_valid:
                # Replace invalid value with a corrected or empty string
                self.delete(0, tk.END)
                self.insert(0, self.get_corrected_value(value))
        return
    
    def get_corrected_value(self, value):
        """
        Returns a corrected value for invalid inputs.
        """
        if self.validation_type == "integer":
            return "".join(filter(str.isdigit, value))
        elif self.validation_type == "positive_integer":
            digits = "".join(filter(str.isdigit, value))
            return digits if digits.isdigit() and int(digits) > 0 else ""
        elif self.validation_type == "float":
            try:
                float(value)
                return value
            except ValueError:
                return ""
        elif self.validation_type == "positive_float":
            try:
                return str(max(0, float(value)))
            except ValueError:
                return ""
        elif self.validation_type == "float_0_1":
            try:
                val = max(0, min(1, float(value)))
                return str(val)
            except ValueError:
                return ""
        elif self.validation_type == "name":
            return self.get_valid_name(value)
        elif self.validation_type == "fromat_xxx":
            return self._validate_format_xxx(value)
        return ""


    def _validate_integer(self, value):
        return value.isdigit() or value == ""

    def _validate_positive_integer(self, value):
        return value.isdigit() and int(value) > 0 or value == ""

    def _validate_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return value == ""

    def _validate_positive_float(self, value):
        try:
            return float(value) > 0 or value == ""
        except ValueError:
            return False

    def _validate_float_0_1(self, value):
        try:
            return 0 <= float(value) <= 1 or value == ""
        except ValueError:
            return False

    def _validate_name(self, value):
        return value == self.get_valid_name(value) or value == ""

    def get_valid_name(self, value):
        # Filter only valid characters and remove spaces
        corrected_value = ''.join(char for char in value if char in self.valid_chars and not char.isspace())
        return corrected_value
    
    def _validate_format_xxx(self, value):
        """
        Validates if the current entry value matches the format XXX (a positive integer with exactly 3 digits).

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if the value matches the format, False otherwise.
        """
        return value.isdigit() and len(value) == 3

