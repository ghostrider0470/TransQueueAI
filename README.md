
# Translation Queue System

## Overview

This system is designed to automate the process of translating text using OpenAI's GPT-3.5 Turbo. The system reads `.po` files, sends the text for translation, and then writes the translated text back to `.po` files.

## Files

### config.py

- Contains the configuration settings for the application.
- Loads environment variables.

### entries.py

- Defines `Entry` and `Entries` classes.
- Handles the text entries and their translations.

### files.py

- Contains functions for handling file operations.
- Reads `.po` files and writes translated entries to them.

### helper.py

- Provides utility functions for string and JSON manipulation.

### main.py

- Orchestrates the entire translation flow.
- Uses multithreading for efficient processing.

## How To Run

1. Make sure you have all the required environment variables set.
2. Run `main.py`.

## Changelog

- Implemented task queue for handling translation tasks.
- The progress is now stored in `progress.json`.
- Improved error-handling mechanisms.
- Fully commented the source code for better readability.

