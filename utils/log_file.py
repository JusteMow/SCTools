import os
from datetime import datetime
import states.states as states
import sys

#Manage the logs: 
def log_entry(new_entry, flush_now=True):
    """
        Args:  line, flush true or false
    """
    instance = LogBufferSingleton.get_instance()
    timestamp = datetime.now().strftime("%y%m%d %H:%M")
    new_log_entry = f"{timestamp} - {new_entry}"
    instance.buffer.append(new_log_entry)
   
    # Efface la barre de progression temporairement
    sys.stdout.write("\r")
    sys.stdout.flush()
    
    # Affiche le message dans stderr
    print(new_log_entry, file=sys.stderr)

    if flush_now:
        flush()

def log_clone(old_filepath, new_filepath):
    """
        Args:  line, flush true or false
    """
    old_relative_file_path  = os.path.relpath(old_filepath, states.root_path)
    new_relative_file_path  = os.path.relpath(new_filepath, states.root_path)
    new_log_entry = f"Clone {old_relative_file_path} to {new_relative_file_path}"
    log_entry(new_log_entry, True)

def log_rename_file(old_filepath, new_filepath):
    """
        Args:  line, flush true or false
    """
    old_relative_file_path  = os.path.relpath(old_filepath, states.root_path)
    new_relative_file_path  = os.path.relpath(new_filepath, states.root_path)
    new_log_entry = f"rename file : {old_relative_file_path} to {new_relative_file_path}"
    log_entry(new_log_entry, True)

def log_stuff(text, old_filepath, new_filepath, flush_now=False):
    """
        Args:  line, flush true or false
    """
    old_relative_file_path  = os.path.relpath(old_filepath, states.root_path)
    new_relative_file_path  = os.path.relpath(new_filepath, states.root_path)
    new_log_entry = f"{text} - {old_relative_file_path} -> {new_relative_file_path}"
    log_entry(new_log_entry, flush_now)

def log_gamebox_change(line, property_name, old_value, new_value, flush_now=False):
    """
    Loggue une modification dans le buffer.
    """
    relative_file_path = "" if states.root_path =="" or states.opened_gamebox == "" else os.path.relpath(states.opened_gamebox, states.root_path)
    new_log_entry = f"{relative_file_path} - Line: {line or 'N/A'} - Property: {property_name} - Old: {old_value} - New: {new_value}"

    log_entry(new_log_entry, flush_now)

def flush():
    """
    Écrit tous les logs dans le fichier, dans l'ordre inverse, en insérant les nouvelles entrées en haut.
    """
    instance = LogBufferSingleton.get_instance()
    if not instance.buffer:
        return
    try:
        # Lire le contenu existant du fichier
        if os.path.exists(instance.log_file_path):
            with open(instance.log_file_path, "r", encoding="utf-8") as log_file:
                existing_content = log_file.read()
        else:
            existing_content = ""

        # Écrire les nouvelles entrées suivies de l'ancien contenu
        with open(instance.log_file_path, "w", encoding="utf-8") as log_file:
            for log_entry in reversed(instance.buffer):
                log_file.write(log_entry + "\n")
            log_file.write(existing_content)

        # Vider le buffer après l'écriture
        instance.buffer.clear()

    except Exception as e:
        print(f"Error while flushing logs: {e} log file may not be updated")

class LogBufferSingleton:
    _instance = None  # Variable de classe pour stocker l'instance unique

    def __init__(self, log_file_path):
        if LogBufferSingleton._instance is not None:
            raise RuntimeError("Use get_instance() to access the singleton instance.")
        self.log_file_path = log_file_path
        self.buffer = []

    @classmethod
    def get_instance(cls):
        """
        Retourne l'instance unique du singleton. Si elle n'existe pas, elle est créée.
        """
        if cls._instance is None:
            if states.root_path == "":
                raise ValueError("log_file_path must be provided when initializing for the first time.")
            log_file_path = os.path.join(states.root_path, "sctool.log")
            cls._instance = cls(log_file_path)
        return cls._instance


def debug(str): 
    """
    print only if debug mode
    """
    if (states.debug_mode):
        print (str)

import time



