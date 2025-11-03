from tkinter import messagebox
import utils.log_file as log

root_path = ""
found_error=False
found_warning = False
debug_mode = False
progress_bar = 0 
opened_gamebox = ""
end_process_log = []

# Global NoticeLabel instance (initialized in main.py)
notice_label = None

def reset_errors ():
    global found_error
    found_error = False
    global found_warning
    found_warning = False

def get_errors():
    """
    returns true if errors found
    """
    global found_error
    global found_warning
    return found_error, found_warning

def set_error_found(text = ""):
    global found_error
    log.log_entry(f"!!! Error Found !!! {text} ")
    found_error = True

def set_warning_found(text = ""): 
    global found_warning
    log.log_entry(f"!!! Warning - may be a normal behaviour !!! {text} ")
    found_warning = True
