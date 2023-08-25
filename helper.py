import json


class StringUtils:
    @staticmethod
    def remove_empty_lines(input_string):
        lines = input_string.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        cleaned_string = "\n".join(non_empty_lines)
        return cleaned_string

    @staticmethod
    def convert_to_json(translations_list):
        translations_dict = {
            lang: translation for lang, translation in translations_list
        }
        translations_json = json.dumps(translations_dict, ensure_ascii=False, indent=4)
        return translations_json
