# BashAI

BashAI is a Python program that uses the OpenAI API to provide users with Bash commands in response to queries. BashAI interacts with users in a conversational manner and provides structured JSON responses that include a command to execute, an explanation of the command, and any relevant notes.
##Dependencies

- Python 3
- OpenAI API
- termcolor

## Installation

1. Install Python 3 if it is not already installed on your system.
2. Install the termcolor library by running the following command:

        pip install termcolor

3. Set your OpenAI API key as an environment variable named OPENAI_API_KEY_BASHAI.

## Usage

To use BashAI, run the following command in your terminal:

        ./bashai.py "<your query>"

Replace <your query> with your query. BashAI will then use the OpenAI API to generate a Bash command in response to your query. BashAI will display the command along with an explanation of the command and any relevant notes.

You will be prompted to confirm whether or not you want to execute the command. If you choose to execute the command, you will be prompted to confirm whether or not you want to use sudo to execute the command.

## Add to PATH (optional)

To make it possible to run bashai.py from anywhere in the terminal, you can add it to a directory that is already in your system's PATH. Here's how:

1. Save a copy without the .py extension.
  
2. Find out where your system stores executables by running the following command:

        echo $PATH

This will output a list of directories separated by colons. These are the directories that your system searches for executables when you run a command in the terminal.

3. Choose one of the directories listed in the output of the previous command, and copy the bashai.py file to that directory. For example, if the output of the previous command includes /usr/local/bin, you can copy the bashai.py file to that directory by running the following command:

        sudo cp bashai /usr/local/bin

Note that you will need to use sudo to copy the file to this directory because it is owned by root.

4. Make the bashai.py file executable by running the following command:

        sudo chmod +x /usr/local/bin/bashai.py

This command grants executable permission to the bashai.py file.

5. Verify that you can run the bashai.py file from anywhere in the terminal by running the following command:

        bashai.py "<your query>"

If everything is set up correctly, BashAI should generate a Bash command in response to your query.

Congratulations, you can now run BashAI from anywhere in the terminal!
