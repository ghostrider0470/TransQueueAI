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
            "content": 'Task: Translate accounting text from DE, FR, EN to BS.\nInput: JSON with text in DE, FR, EN.\nOutput: JSON with text in BS.'
        },
        {"role": "user", "content": entries},
    ]

    return context


def request_translation(context):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=context,
        temperature=1,
        max_tokens=10000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    content = response["choices"][0]["message"]["content"].strip()
    translation_json = json.loads(content)  # Parse the JSON response
    bosnian_translation = translation_json.get("bs", "")  # Extract the Bosnian translation

    return bosnian_translation
