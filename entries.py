# entries.py
import os

import openai
import json

class Entry:
    def __init__(self, msgid):
        self.translations = {}

    def __setitem__(self, key, value):
        self.translations[key] = value

    def __getitem__(self, key):
        return self.translations.get(key, None)

    def to_dict(self):
        return self.translations

    @classmethod
    def from_dict(cls, dict_obj):
        entry = cls()
        entry.translations = dict_obj
        return entry

    def add_translation(self, lang, translation):
        self.translations[lang] = translation

    def get_translation(self, lang):
        return self.translations.get(lang, "")

    def as_dict(self):
        return self.translations

    def to_dict(self):
        return self.translations

    @classmethod
    def from_dict(cls, dict_obj):
        entry = cls()
        entry.translations = dict_obj
        return entry
class Entries:
    def __init__(self):
        self.entries = {}  # The keys are msgids, and the values are Entry objects

    def __len__(self):
        return len(self.entries)


    def add_entry(self, entry):
        self.entries[entry.msgid] = entry

    def get_entry(self, msgid):
        return self.entries.get(msgid)

    def get_entries(self):
        return self.entries.items()

    def add_translation(self, key, lang, translation):
        if key not in self.entries:
            self.entries[key] = {}
        self.entries[key][lang] = translation

    def get_translation(self, key, lang):
        return self.entries.get(key, {}).get(lang)

    def as_dict(self):
        return self.entries

    @classmethod
    def from_dict(cls, dict_obj):
        entries = cls()
        entries.entries = dict_obj
        return entries


def create_context(entries):
    context = [
        {
            "role": "system",
            "content": 'Task:\nYou are an advanced AI Translator. Analyze the text content of JSON and its different entries (German, French, and English) to understand the context and meaning. Then, provide a translation in Bosnian using Bosnian accounting terms.\n\nInput:\n\n{\n    "de": "\\n\\nDie Buchungszeile (%s) ist nicht ausgeglichen. Die Summe der Belastungen liegt bei %s und die Summe der Gutschriften liegt bei %s. \\nSie können ein Standardkonto im Journal „%s“ angeben, um jede Buchungszeile automatisch auszugleichen.",\n    "fr": "\\n\\nL\'écriture (%s) n\'est pas équilibrée.\\nLe total des débits est égal à %s et le total des crédits est égal à %s.\\nVous voudrez peut-être spécifier un compte par défaut sur le journal \\"%s\\" pour équilibrer automatiquement chaque mouvement.",\n    "en": "\\n\\nThe move (%s) is not balanced.\\nThe total of debits equals %s and the total of credits equals %s.\\nYou might want to specify a default account on journal \\"%s\\" to automatically balance each move."\n}\n\n\nOutput:\n\n{\n    "bs": "\\n\\nObračun(%s) nije uravnotežen.\\nUkupno zaduženje iznosi %s, a ukupno odobrenje iznosi %s.\\nMožda ćete htjeti odrediti zadani račun u dnevniku \\"%s\\" kako biste automatski uravnotežili svaki potez."\n}\n\n\nThe provided output is a valid translation of the given text into Bosnian, adhering to the accounting context specified in the task.',
        },
        {"role": "user", "content": entries},
    ]
    return context


def request_translation(context):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    content = response["choices"][0]["message"]["content"].strip()
    translation_json = json.loads(content)  # Parse the JSON response
    bosnian_translation = translation_json.get("bs", "")  # Extract the Bosnian translation

    return bosnian_translation
