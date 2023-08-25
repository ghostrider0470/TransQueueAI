import os

from tqdm import tqdm

import translations
from config import Config
from files import load_progress, load_po_files, save_progress, create_po_file
from helper import StringUtils

config = Config()

if __name__ == "__main__":
    progress_file = "output/progress.json"
    translations_by_key, start_index = load_progress(progress_file)

    if translations_by_key is None:
        translations_by_key = load_po_files(config.input_directory)

    items = list(translations_by_key.entries())

    with tqdm(total=len(translations_by_key), desc="Translating", ascii=True) as pbar:
        # Set the progress bar to the starting index
        pbar.n = start_index
        pbar.last_print_n = start_index
        pbar.refresh()

        for i, (msgId, translation_dict) in enumerate(
            items[start_index:], start=start_index
        ):
            minified_msgId = StringUtils.remove_empty_lines(msgId)
            translations_string = StringUtils.convert_to_json(translation_dict)

            context = translations.create_context(translations_string)
            response = translations.request_translation(context)

            # Extracting Bosnian translation and updating translations_by_key
            bosnian_translation = response
            translations_by_key.add_translation(msgId, "bs", bosnian_translation)

            # Save progress at every iteration
            save_progress(translations_by_key, i + 1, progress_file)
            pbar.update(1)

    # Creating .po file for Bosnian translations
    output_directory = os.path.join(config.app_root_directory, "output")
    create_po_file(translations_by_key, "bs", output_directory)