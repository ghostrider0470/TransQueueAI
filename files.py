# files.py
import glob
import json
import os
from queue import Queue

import polib

from entries import Entries, Entry


def save_progress(entries, task_queue, path="progress.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"entries": entries.entries, "task_queue": list(task_queue.queue)}, f, indent=4)

def load_progress(path="progress.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            entries = Entries().from_dict(data['entries'])
            task_queue = Queue()
            for item in data.get("task_queue", []):
                task_queue.put(item)
            return entries, task_queue
    return None, Queue()




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

                    # if msgid not in entries.entries:
                    #     new_entry = Entry(msgid)
                    #     entries.add_entry(new_entry)

                    entries.add_translation(msgid, lang, translation)

    return entries





def create_po_file(entries_by_key, lang,input_directory, output_directory, current_sub_directory):
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
        # entry = polib.POEntry(msgid=key, msgstr=translation_for_lang)
        try:
            po.find(key).msgstr = translation_for_lang
        except:
            print(key)
            entry = polib.POEntry(msgid=key, msgstr=translation_for_lang)


    output_file_path = os.path.join(output_directory, current_sub_directory, f"{lang}.po")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    po.save(output_file_path)
    print(f"{output_file_path} saved successfully.")
