# files.py
import glob
import json
import os

import polib

from translations import Translations


def save_progress(translations, index, path="progress.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"translations": translations.to_json(), "index": index}, f)


def load_progress(path="progress.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            translations = Translations.from_json(data["translations"])
            return translations, data["index"]
    return None, 0


def load_po_files(input_directory):
    translations = Translations()

    for root, dirs, _ in os.walk(input_directory):
        for directory in dirs:
            path = os.path.join(root, directory)
            files = glob.glob(os.path.join(path, "*.po"))

            for file_path in files:
                if 'template' in os.path.basename(file_path):
                    continue  # Skip template files

                po_file = polib.pofile(file_path)
                lang = po_file.metadata.get("Language", "unknown")

                for entry in po_file:
                    key = entry.msgid
                    translation = entry.msgstr
                    translations.add_translation(key, lang, translation)

    return translations





def create_po_file(translations_by_key, lang,input_directory, output_directory, current_sub_directory):
    # Find the template file in the current_sub_directory
    template_files = glob.glob(os.path.join(input_directory, current_sub_directory, "template*.po"))
    template_path = template_files[0] if template_files else None

    if template_path:
        po = polib.pofile(template_path)
    else:
        po = polib.POFile()

    po.metadata = {"Language": lang}

    for key, translations in translations_by_key.items():
        translation_for_lang = translations.get(lang, "")
        entry = polib.POEntry(msgid=key, msgstr=translation_for_lang)
        po.append(entry)

    output_file_path = os.path.join(output_directory, current_sub_directory, f"{lang}.po")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    po.save(output_file_path)
    print(f"{output_file_path} saved successfully.")
