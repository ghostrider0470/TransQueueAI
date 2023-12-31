
# files.py

import glob
import json
import os
from queue import Queue
import polib

from entries import Entries, Entry

# Function to save the progress of translations and the state of the task queue
def save_progress(entries, task_queue, path="progress.json"):
    with open(path, "w", encoding="utf-8") as f:
        # Convert the task_queue to a list and save it along with entries
        queue_list = list(task_queue.queue)
        json.dump({"entries": entries.entries, "task_queue": queue_list}, f, indent=4)

# Function to load the progress of translations and the state of the task queue
def load_progress(path="progress.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            entries = Entries().from_dict(data['entries'])
            task_queue = Queue()
            # Populate the task_queue from the saved state
            for item in data.get("task_queue", []):
                task_queue.put(item)
            return entries, task_queue
    return None, Queue()

# Function to load .po files and populate the Entries object
def load_po_files(input_directory):
    entries = Entries()
    for root, dirs, _ in os.walk(input_directory):
        for directory in dirs:
            path = os.path.join(root, directory)
            files = glob.glob(os.path.join(path, "*.po"))
            for file_path in files:
                if 'template' in os.path.basename(file_path):
                    continue  # Skip template files
                po_file = polib.pofile(file_path)
                for entry in po_file:
                    msgid = entry.msgid
                    lang = po_file.metadata.get("Language", "en")
                    translation = entry.msgstr
                    entries.add_translation(msgid, lang, translation)
    return entries

# Function to create a .po file for a specific language
def create_po_file(entries_by_key, lang, input_directory, output_directory, current_sub_directory):
    # Find the template file in the current_sub_directory
    template_files = glob.glob(os.path.join(input_directory, current_sub_directory, "template*.po"))
    template_path = template_files[0] if template_files else None
    if template_path:
        po = polib.pofile(template_path)
    else:
        po = polib.POFile()
    po.metadata = {"Language": lang}
    for key, entries in entries_by_key.get_entries():
        translation_for_lang = entries.get(lang, "")
        try:
            po.find(key).msgstr = translation_for_lang
        except:
            entry = polib.POEntry(msgid=key, msgstr=translation_for_lang)
            po.append(entry)
    output_file_path = os.path.join(output_directory, current_sub_directory, f"{lang}.po")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    po.save(output_file_path)
    print(f"{output_file_path} saved successfully.")
