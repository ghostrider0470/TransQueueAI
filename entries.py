
# entries.py

import os
import openai
import json

class Entry:
    def __init__(self, msgid):
        # Initialize an entry with a dictionary to hold translations
        self.translations = {}

    def __setitem__(self, key, value):
        # Add a translation
        self.translations[key] = value

    def __getitem__(self, key):
        # Retrieve a translation
        return self.translations.get(key, None)

    def to_dict(self):
        # Convert the translations to a dictionary
        return self.translations

    @classmethod
    def from_dict(cls, dict_obj):
        # Create an Entry object from a dictionary
        entry = cls("")
        entry.translations = dict_obj
        return entry

    def add_translation(self, lang, translation):
        # Add a translation for a specific language
        self.translations[lang] = translation

    def get_translation(self, lang):
        # Get a translation for a specific language
        return self.translations.get(lang, "")

    def as_dict(self):
        # Convert to dictionary format
        return self.translations

class Entries:
    def __init__(self):
        # Initialize with a dictionary to hold Entry objects
        self.entries = {}

    def __len__(self):
        # Return the number of entries
        return len(self.entries)

    def add_entry(self, entry):
        # Add an Entry object to the dictionary
        self.entries[entry.msgid] = entry

    def get_entry(self, msgid):
        # Retrieve an Entry object based on its msgid
        return self.entries.get(msgid)

    def get_entries(self):
        # Retrieve all entries as a list of items
        return self.entries.items()

    def add_translation(self, key, lang, translation):
        # Add a translation for a specific language and msgid (key)
        if key not in self.entries:
            self.entries[key] = {}
        self.entries[key][lang] = translation

    def get_translation(self, key, lang):
        # Get a translation based on its msgid (key) and language
        return self.entries.get(key, {}).get(lang)

    def as_dict(self):
        # Convert to dictionary format
        return self.entries

    @classmethod
    def from_dict(cls, dict_obj):
        # Create an Entries object from a dictionary
        entries = cls()
        entries.entries = dict_obj
        return entries

# Function to create the context for translation request
def create_context(entries):
    context = [
        {
            "role": "system",
            "content": 'Task: Translate accounting text from DE, FR, EN to BS.\nInput: JSON with text in DE, FR, EN.\nOutput: JSON with text in BS.'
        },
        {"role": "user", "content": entries},
    ]
    return context

# Function to request translation from OpenAI
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
    translation_json = json.loads(content)
    bosnian_translation = translation_json.get("bs", "")
    return bosnian_translation
