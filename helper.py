
# helper.py

import json

# Class to hold utility functions for string manipulation
class StringUtils:
    @staticmethod
    def remove_empty_lines(input_string):
        # Remove empty lines from the string
        lines = input_string.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        cleaned_string = "\n".join(non_empty_lines)
        return cleaned_string

    @staticmethod
    def convert_to_json(translation_dict):
        # Convert a translation dictionary to a JSON-formatted string
        entries_dict = {
            lang: translation for lang, translation in translation_dict.items()
        }
        entries_json = json.dumps(entries_dict, ensure_ascii=False, indent=4)
        return entries_json
