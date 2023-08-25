import os

import openai
import json


class Translations:
    def __init__(self):
        self.length = len(self)
        self.translations = {"msgId": {"languages": {"en": "", "se": ""}}}

    def __len__(self):
        return len(self.translations)

    def to_json(self):
        entries = [
            {"id": key, "translations": value}
            for key, value in self.translations.items()
        ]
        return json.dumps({"entries": entries}, indent=4)

    @classmethod
    def from_json(cls, json_str):
        obj = cls()
        obj.translations = json.loads(json_str)
        return obj

    def add_translation(self, key, lang, translation):
        if key not in self.translations:
            self.translations[key] = {}
        self.translations[key][lang] = translation

    def get_translation(self, key, lang):
        return self.translations.get(key, {}).get(lang)

    def entries(self):
        return self.translations.items()

    def as_dict(self):
        return self.translations


def create_context(translations):
    context = [
        {
            "role": "system",
            "content": 'Task:\nYou are an advanced AI Translator. Analyze the text content of JSON and its different translations (German, French, and English) to understand the context and meaning. Then, provide a translation in Bosnian using Bosnian accounting terms.\n\nInput:\n\n{\n    "de": "\\n\\nDie Buchungszeile (%s) ist nicht ausgeglichen. Die Summe der Belastungen liegt bei %s und die Summe der Gutschriften liegt bei %s. \\nSie können ein Standardkonto im Journal „%s“ angeben, um jede Buchungszeile automatisch auszugleichen.",\n    "fr": "\\n\\nL\'écriture (%s) n\'est pas équilibrée.\\nLe total des débits est égal à %s et le total des crédits est égal à %s.\\nVous voudrez peut-être spécifier un compte par défaut sur le journal \\"%s\\" pour équilibrer automatiquement chaque mouvement.",\n    "en": "\\n\\nThe move (%s) is not balanced.\\nThe total of debits equals %s and the total of credits equals %s.\\nYou might want to specify a default account on journal \\"%s\\" to automatically balance each move."\n}\n\n\nOutput:\n\n{\n    "bs": "\\n\\nObračun(%s) nije uravnotežen.\\nUkupno zaduženje iznosi %s, a ukupno odobrenje iznosi %s.\\nMožda ćete htjeti odrediti zadani račun u dnevniku \\"%s\\" kako biste automatski uravnotežili svaki potez."\n}\n\n\nThe provided output is a valid translation of the given text into Bosnian, adhering to the accounting context specified in the task.',
        },
        {"role": "user", "content": translations},
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
    bosnian_translation = translation_json.get(
        "bs", ""
    )  # Extract the Bosnian translation

    return bosnian_translation
