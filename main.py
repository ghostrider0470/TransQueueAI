
# main.py

import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue
import time
from tqdm import tqdm

from files import load_progress, save_progress, load_po_files, create_po_file
from helper import StringUtils
from entries import create_context, request_translation
from config import Config

# Initialize configuration and lock for thread-safe operations
config = Config()
lock = Lock()
task_queue = Queue()

# Function to process translation tasks
def process_translation(translations_by_key, progress_file, pbar):
    while not task_queue.empty():
        msgId, translation_dict = task_queue.get()
        retries = 50
        delay = 5
        for attempt in range(retries):
            try:
                minified_msgId = StringUtils.remove_empty_lines(msgId)
                translations_string = StringUtils.convert_to_json(translation_dict)
                context = create_context(translations_string)
                bosnian_translation = request_translation(context)
                translations_by_key.add_translation(msgId, "bs", bosnian_translation)

                # Save progress and update the progress bar
                with lock:
                    save_progress(translations_by_key, task_queue, progress_file)
                pbar.update(1)
                break
            except Exception as e:
                if "Rate limit reached" in str(e):
                    time.sleep(delay)
                    delay *= 2
                else:
                    print(f"An error occurred while translating msgId {{msgId}}: {{e}}")
                    break
        if attempt == retries - 1:
            task_queue.put((msgId, translation_dict))

# Function to process directories and create .po files
def process_directory(directory, translations_by_key, input_directory, output_directory):
    create_po_file(translations_by_key, "bs", input_directory, output_directory, directory)

# Main execution starts here
if __name__ == "__main__":
    progress_file = "output/progress.json"
    translations_by_key, task_queue = load_progress(progress_file)

    if translations_by_key is None:
        translations_by_key = load_po_files(config.input_directory)
        for msgId, translation_dict in translations_by_key.get_entries():
            task_queue.put((msgId, translation_dict))

    # Initialize the progress bar
    with tqdm(total=task_queue.qsize(), desc="Translating", ascii=True) as pbar:
        with ThreadPoolExecutor() as executor:
            executor.submit(process_translation, translations_by_key, progress_file, pbar)

    # Process each directory to create .po files
    output_directory = os.path.join(config.app_root_directory, "output")
    directories = []
    for root, dirs, _ in os.walk(config.input_directory):
        directories.extend(dirs)
    with ThreadPoolExecutor() as executor:
        executor.map(process_directory, directories, [translations_by_key]*len(directories), [config.input_directory]*len(directories), [output_directory]*len(directories))
