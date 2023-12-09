#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import logging
from termcolor import colored
import openai
from dotenv import load_dotenv
from halo import Halo

MAX_LINE_WIDTH = 80

# Logger configuration
logging.basicConfig(filename='bai.log', level=logging.ERROR)
logger = logging.getLogger(__name__)

# Spinner configuration
spinner = Halo(text='Waiting for response...', spinner='dots12')

def wrap_string(s, width):
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

def get_system_info():
    try:
        # Command to get kernel version
        kernel_version = subprocess.check_output('uname -r', shell=True).decode().strip()

        # Command to get distribution name and version
        os_release = subprocess.check_output('cat /etc/os-release', shell=True).decode()

        # Parsing /etc/os-release for NAME and VERSION_ID
        distro_name = None
        distro_version = None
        for line in os_release.split('\n'):
            if line.startswith('NAME='):
                distro_name = line.split('=')[1].strip('"')
            if line.startswith('VERSION_ID='):
                distro_version = line.split('=')[1].strip('"')

        return {
            "Kernel Version": kernel_version,
            "Distro Name": distro_name,
            "Distro Version": distro_version
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting system info: {e}")
        print(f"Error getting system info: {e}")
        return None

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
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY_BASHAI")
    if not api_key:
        logger.error("OPENAI_API_KEY_BASHAI environment variable is not set.")
        print("Error: The OPENAI_API_KEY_BASHAI environment variable is not set.")
        sys.exit(1)
    return api_key

def call_openai_api(api_key, query, system_info):
    openai.api_key = api_key
    system_content = f"You are now an expert human to bash interpreter for {system_info['Distro Name']} {system_info['Distro Version']} that only responds with commands and does not use markup."
    user_content = f"You are now an expert human to bash interpreter for {system_info['Distro Name']} {system_info['Distro Version']}. I will tell you what I want to do and you will show me the commands to execute. Respond in JSON structured text with three keys only: 'Explanation': with an explanation and any relevant related switches or options, 'Command': the command/s or script, and 'Notes': any additional info. Do not offer any commentary or explanations outside of the JSON. Use tabs and newlines but do not use markup. My query is: {query}"
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
    for line in wrap_string(explanation, MAX_LINE_WIDTH):
        print(colored(line, "white"))
    print(colored("\nNOTES:", "red"))
    notes_lines = wrap_string(notes, MAX_LINE_WIDTH)
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

    system_info = get_system_info()
    if not system_info:
        print("Unable to determine system information.")
        sys.exit(1)

    spinner.start()
    response = call_openai_api(api_key, sys.argv[1], system_info)
    result = process_response(response)
    spinner.stop()

    command = print_response(result)
    run_command(command)

if __name__ == "__main__":
    main()
