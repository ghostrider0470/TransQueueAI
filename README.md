# TransQueueAI

## Description
TransQueueAI is a Python-based automated translation queue system that leverages OpenAI's GPT-3.5 Turbo model. This system is designed to handle large-scale text translation tasks, ensuring efficient operation and fault tolerance. 

## Features
- **Parallelized Translation**: Takes advantage of Python's threading capabilities to speed up the translation process.
- **Rate-Limit Handling**: Automatically retries translation tasks when API rate limits are reached.
- **Progress Tracking**: Keeps track of the translation progress and resumes from where it left off.
- **Queue Persistence**: Stores the task queue in a JSON file so the program can be safely stopped and resumed.

## Installation
1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Rename `.env.example` to `.env` and update it with your OpenAI API Key and other configurations.

## Usage
1. Add your `.po` files in the `input` directory.
2. Run `main.py` to start the translation process.

## How it Works
- The translation tasks are placed in a queue.
- Multiple threads pick tasks from the queue and send them to the OpenAI GPT-3.5 Turbo model for translation.
- The translated text is then stored and the queue is updated.
- All progress is saved in a `progress.json` file.

## Contributing
We welcome contributions! Please see the `CONTRIBUTING.md` for details.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
