import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue
import time
from tqdm import tqdm
from files import load_progress, save_progress, load_po_files, create_po_file
from helper import StringUtils
import entries
from config import Config

config = Config()

lock = Lock()
task_queue = Queue()

def process_translation(translations_by_key, progress_file):
    while not task_queue.empty():
        msgId, translation_dict = task_queue.get()
        retries = 3  
        delay = 5  

        for attempt in range(retries):
            try:
                minified_msgId = StringUtils.remove_empty_lines(msgId)
                translations_string = StringUtils.convert_to_json(translation_dict)
                context = entries.create_context(translations_string)
                response = entries.request_translation(context)

                with lock:
                    bosnian_translation = response
                    translations_by_key.add_translation(msgId, "bs", bosnian_translation)
                    save_progress(translations_by_key, task_queue, progress_file)

                break  
            except Exception as e:
                if "Rate limit reached" in str(e):
                    time.sleep(delay)
                    delay *= 2  
                else:
                    print(f"An error occurred while translating msgId {msgId}: {e}")
                    break

        if attempt == retries - 1:
            task_queue.put((msgId, translation_dict))

def process_directory(directory, translations_by_key, input_directory, output_directory):
    create_po_file(translations_by_key, "bs", input_directory, output_directory, directory)

if __name__ == "__main__":
    progress_file = "output/progress.json"
    translations_by_key, task_queue = load_progress(progress_file)

    if translations_by_key is None:
        translations_by_key = load_po_files(config.input_directory)
        for msgId, translation_dict in translations_by_key.get_entries():
            task_queue.put((msgId, translation_dict))

    with tqdm(total=task_queue.qsize(), desc="Translating", ascii=True) as pbar:
        with ThreadPoolExecutor() as executor:
            executor.submit(process_translation, translations_by_key, progress_file)

        pbar.update(task_queue.qsize())

    output_directory = os.path.join(config.app_root_directory, "output")
    directories = []
    for root, dirs, _ in os.walk(config.input_directory):
        directories.extend(dirs)

    with ThreadPoolExecutor() as executor:
        executor.map(process_directory, directories, [translations_by_key]*len(directories), [config.input_directory]*len(directories), [output_directory]*len(directories))
