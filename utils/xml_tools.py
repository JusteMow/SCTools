import os
from datetime import datetime
import re
from lxml import etree
import states.states as states
import utils.log_file as log

def get_root(file_path):
    # Step 1: Clean and parse content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = check_invalid_char(file.read())

    parser = etree.XMLParser(remove_blank_text=False)
    root = etree.XML(content.encode('utf-8'), parser)

    states.opened_gamebox=file_path
    return root

def get_root_in_gamebox(file_path, recover=False):
    # Step 1: Clean and parse content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = check_invalid_char(file.read())

    wrapped_content = f"<root>{content}</root>"  # Temporary root for parsing
    parser = etree.XMLParser(remove_blank_text=False, recover = recover)
    root = etree.XML(wrapped_content.encode('utf-8'), parser)

    states.opened_gamebox=file_path
    return root

def preprocess_and_load(xml_file):
    """
    Prétraiter le pseudo-XML en supprimant les attributs en doublon, puis le charger.
    """
    cleaned_lines = []
    duplicated_values = []  # Sauvegarde des doublons supprimés

    with open(xml_file, "r", encoding="utf-8") as file:
        for line in file:
            # Identifier les attributs doublons avec une regex
            match = re.search(r'(ForceFielduseLife\s*=\s*".*?")', line)
            if match:
                attr = match.group(1)
                if line.count(attr) > 1:
                    # Supprimer les doublons
                    line = line.replace(attr, "", 1)  # Garder la première occurrence
                    duplicated_values.append(attr)  # Sauvegarder pour réinsertion
            cleaned_lines.append(line)

    # Sauvegarder le fichier nettoyé pour modification
    cleaned_xml = "cleaned_gamebox.xml"
    with open(cleaned_xml, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)
    # log.log_entry(f"{file} cleared and processesd" )

    return cleaned_xml, duplicated_values


def reinject_duplicates(updated_content, duplicated_values):
    """
    Réinjecter les valeurs doublons dans le contenu modifié (sous forme de chaîne).

    Args:
        updated_content (str): Le contenu modifié (XML transformé sous forme de chaîne).
        duplicated_values (list): Liste des attributs doublons à réinjecter.

    Returns:
        str: Le contenu final avec les doublons réinjectés.
    """
    content = updated_content
    for value in duplicated_values:
        # Réinjecter chaque doublon à la fin de la première balise correspondante
        content = re.sub(r'(/?>)', f' {value}\1', content, count=1)

    log.debug("Doublons réinjectés.")
    return content
	

def check_invalid_char(content):
    """
    Cleans the XML-like content to handle common issues such as invalid characters.
    Replaces invalid characters with '0'.
    """
    # Replace problematic characters with '0'
    content = re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '0', content)
    return content

from lxml import etree

def clone_element(element):
    """
    Deep Clones an lxml element, including all its attributes, text, and children.

    Args:
        element (etree.Element): The element to clone.

    Returns:
        etree.Element: A new cloned element.
    """
    # Crée un nouvel élément avec le même tag et les mêmes attributs
    new_element = etree.Element(element.tag, attrib=element.attrib)

    # Copie le texte et la queue
    new_element.text = element.text
    new_element.tail = element.tail

    # Clone récursivement les enfants
    for child in element:
        new_element.append(clone_element(child))

    return new_element



#Set properties in XML and log to console and logfile		
def set_property_with_log(element, property_name, new_value):
    """
    Set a property on an XML element and log the change.

    Args:
        element (etree.Element): The XML element to modify.
        property_name (str): The attribute name to set.
        new_value (str): The new value for the attribute.
        file_name (str): The name of the file being modified.
    """
    try:
        # Get the old value of the property
        old_value = element.get(property_name)
        if old_value != new_value:  # Only log if the value is actually changed
            element.set(property_name, new_value)
            # Log the change using sourceline if available
            log.log_gamebox_change(
                line=element.sourceline if hasattr(element, 'sourceline') else None,
                property_name=property_name,
                old_value=old_value,
                new_value=new_value,
            )
    except Exception as e:
        states.set_error_found(f"Error setting property {property_name} on element: {element} : {e}")

#unused
def replace_and_log(content, old_name, new_name, file_path):
    """
    Replaces all occurrences of old_name with new_name in the content and logs the changes.

    Args:
        content (str): The original content of the file.
        old_name (str): The string to replace.
        new_name (str): The replacement string.
        file_path (str): The full file path of the file being processed.

    Returns:
        tuple: (updated_content (str), replacements (int))
    """
    replacements = 0
    updated_lines = []


    try: 
        for line_number, line in enumerate(content.splitlines(), start=1):
            if old_name in line:
                count = line.count(old_name)
                replacements += count
                updated_line = line.replace(old_name, new_name)

                #log line 
                relative_file_path = os.path.relpath(file_path, states.root_path)
                updated_lines.append(updated_line)

                # Log each replacement
                log_entry = (f"{datetime.now():%y%m%d %H:%M} - File: {relative_file_path} - Line: {line_number} - "
                            f"Replaced: {count} occurrences\n")
                log.log_entry(log_entry, True)
            else:
                updated_lines.append(line)
    except Exception as e:
        error_line = f"Error replacing content for {file_path}: -old : {old_name} - new : {new_name} {e}"
        states.set_error_found(error_line)
        

    updated_content = '\n'.join(updated_lines)
    return updated_content, replacements


#Write content in files 
def write_updated_content(file_path, root):
    try:
        with open(file_path, 'wb') as file:
            file.write(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True))
        log.debug(f"close {file_path} ")
        log.flush()
        states.opened_gamebox=""
        return True
    except Exception as e:
        states.set_error_found(f"Error writing updated content for {file_path}: {e}")
        return False
		
		
def write_updated_wrapped_content(file_path, root):
    """
    Writes the updated content back to the file, removing the added root wrapper.
    
    Args:
        file_path (str): The path of the file to write to.
        root (etree.Element): The root element of the XML tree.
    """
    try:
        # Extract content without the root wrapper
        updated_content = ''.join(etree.tostring(child, encoding='unicode', method='xml') for child in root)
        
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        log.debug(f"close {file_path} ")
        log.flush()
        states.opened_gamebox=""
        return True
    except Exception as e:
        states.set_error_found(f"Error writing updated wrapped content for {file_path}: {e}")
        return False