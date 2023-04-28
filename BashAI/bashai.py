#!/usr/bin/env python3

import openai
import sys
import os
import json
import logging
from termcolor import colored
import subprocess

MAX_LINE_WIDTH = 80

logging.basicConfig(filename='bai.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def wrap_string(s, width):
    # helper function to wrap a string at a given width
    lines = []
    for paragraph in s.split("\n"):
        while len(paragraph) > width:
            pos = paragraph.rfind(' ', 0, width+1)
            if pos <= 0:
                pos = width
            lines.append(paragraph[:pos])
            paragraph = paragraph[pos+1:]
        lines.append(paragraph)
    return lines


def run_command(command):
    run_command = input("Do you want to run this command? (y/n): ")
    if run_command.lower() in ('y', 'yes'):
        use_sudo = input("Do you want to use sudo? (y/n): ")
        if use_sudo.lower() in ('y', 'yes'):
            command = "sudo " + command
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            logger.error(f"Error running command: {e}")
            print(f"Error running command: {e}")

def validate_arguments():
    if len(sys.argv) != 2:
        logger.error("Invalid command line arguments.")
        print("Usage: bai \"<your query>\"")
        sys.exit(1)

def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY_BASHAI")
    if not api_key:
        logger.error("OPENAI_API_KEY_BASHAI environment variable is not set.")
        print("Error: The OPENAI_API_KEY_BASHAI environment variable is not set.")
        sys.exit(1)
    return api_key

def call_openai_api(api_key, query):
    openai.api_key = api_key
    system_content = "You are now an expert human to bash interpreter for Debian 11 that only responds with commands and does not use markup."
    user_content = f"You are now an expert human to bash interpreter for Debian 11. I will tell you what I want to do and you will show me the commands to execute. Respond in JSON structured text with three keys only: 'Explanation': with an explanation and any relevant related switches or options, 'Command': the command/s or script, and 'Notes': any additional info. Do not offer any commentary or explanations outside of the JSON. Use tabs and newlines but do not use markup. My query is: {query}"
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": f"{system_content}"},
                {"role": "user", "content": f"{user_content}"}
            ]
        )
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)
    return response

def process_response(response):
    result = response.choices[0].message.content
    logger.debug(f"Response from OpenAI: {result}")
    try:
        result = json.loads(result)
    except json.JSONDecodeError:
        logger.error(f"Error decoding OpenAI response: {result}")
        print(f"Error decoding OpenAI response: {result}")
        sys.exit(1)
    return result

def print_response(result):
    explanation = result.get('Explanation', '')
    command = result.get('Command', '')
    notes = result.get('Notes', '')
    if not explanation or not command:
        logger.error("Response from OpenAI is missing explanation or command.")
        print("Error: Response from OpenAI is missing explanation or command.")
        sys.exit(1)
    print("\n")
    print(colored("=" * 80, "cyan"))
    print(colored("EXPLANATION:", "green"))
    for line in wrap_string(explanation, 80):
        print(colored(line, "white"))
    print(colored("\nNOTES:", "red"))
    notes_lines = wrap_string(notes, 80)
    if notes_lines:
        print(colored("\n".join(notes_lines), "white"))
    print(colored("=" * 80, "cyan"))
    print(colored("\nCOMMAND:", "green"))
    print(colored(command, "white"))
    print(colored("=" * 80, "cyan"))
    print("\n")
    return command

def main():
    validate_arguments()
    api_key = get_api_key()
    response = call_openai_api(api_key, sys.argv[1])
    result = process_response(response)
    command = print_response(result)
    run_command(command)

if __name__ == "__main__":
    main()
