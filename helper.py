# helper.py
import json


class StringUtils:
    @staticmethod
    def remove_empty_lines(input_string):
        lines = input_string.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        cleaned_string = "\n".join(non_empty_lines)
        return cleaned_string

    @staticmethod
    def convert_to_json(translation_dict):
        entries_dict = {
            lang: translation for lang, translation in translation_dict.items()
        }
        entries_json = json.dumps(entries_dict, ensure_ascii=False, indent=4)
        return entries_json
