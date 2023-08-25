# config.py
import os

import openai
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.transifex_key = os.environ.get("TRANSIFEX_API_KEY")
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.openai_key
        # Get the root directory of the application
        self.app_root_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the input directory located in the root of the application
        self.input_directory = os.path.join(self.app_root_directory, "input")

    # You can add methods to validate or manipulate the keys if necessary
