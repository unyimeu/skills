# Course Skills Extraction Project

This project is designed to extract specific skills from MIT course descriptions using OpenAI's GPT-3.5-turbo model. The project reads course data from a CSV file, creates detailed prompts for each course, and makes asynchronous requests to the OpenAI API to get the skills specific to each course.

## Requirements

- Python 3.7+
- pandas
- openai
- aiohttp
- certifi
- ssl

## Installation

1. Clone this repository.
2. Install the required packages

## Usage

1. Ensure you have your OpenAI API key. You can set it as an environment variable `OPENAI_API_KEY` or insert it directly into the code.

2. Prepare your CSV file (`classes.csv`) with the following columns:
    - `Title`: The name of the course.
    - `Prereqs`: Prerequisites for the course.
    - `Description`: A detailed description of the course.

3. Run the script:
    ```sh
    python your_script_name.py
    ```
