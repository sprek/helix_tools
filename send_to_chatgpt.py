import subprocess
import sys


PATH_TO_AI = "ai"
TMP_FILE = "/tmp/helix_gpt_tmp.txt"
COMMAND_OPTION_TO_DESCRIPTION = {
    "errors": "Find and correct any errors in the provided LANGUAGE code",
    "explain": "Explain the provided LANGUAGE code",
    "optimize": "Show me how to optimize the provided LANGUAGE code",
    "simplify": "Simplify the provided LANGUAGE code",
    "doc": "Write a docstring for the LANGUAGE code",
    "test": "Write a unit test for the provided LANGUAGE function",
    "correct": "The provided code is just a snippet. Do not mention missing imports, functions, or variables. Assume that anything missing has already been defined. Please identify if this LANGUAGE code can be improved. Write a docstring for it if it doesn't already have one.",
    "write": "Write some LANGUAGE code that does the provided instructions",
    "instruct": "The provided LANGUAGE code has instructions on what to do with it in the comment that starts with 'AI:'. Please follow the instructions",
    "words": "Follow the instructions provided",
}


def replace_template_language(message, language):
    if "LANGUAGE" in message:
        return message.replace("LANGUAGE", language)
    return message


def send_to_ai(context, message, tmux_pane):
    """
    Send a message and context to an artificial intelligence agent in a Tmux pane.

    Args:
        context (str): The context to send to the AI agent.
        message (str): The message to send to the AI agent.
        tmux_pane (int): The index of the Tmux pane to send the message in.
    """
    if context == "":
        return
    with open(TMP_FILE, "w") as outf:
        outf.write(context)
    try:
        subprocess.run(
            [
                "tmux",
                "send-keys",
                "-t",
                f"{tmux_pane}",
                f'cat {TMP_FILE} | {PATH_TO_AI} "{message}"\n',
            ]
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running subprocess: {e}")


def print_help():
    """
    Displays the command line arguments expected by this program
    """
    help_message = f"""
    Usage: python send_to_chatgpt.py TMUX_PANE LANGUAGE COMMAND
        - TMUX_PANE: The number of the tmux pane to use
        - LANGUAGE: The programming language to use (e.g. python, java)
        - COMMAND: The command to execute ({", ".join(COMMAND_OPTION_TO_DESCRIPTION.keys())})
    """
    print(help_message)


def main():
    if not len(sys.argv) == 4:
        print("Invalid number of arguments")
        print_help()
        sys.exit(1)
    tmux_pane = sys.argv[1]
    language = sys.argv[2]
    command = sys.argv[3]
    if command in COMMAND_OPTION_TO_DESCRIPTION.keys():
        if sys.stdin.isatty():
            print("No data piped in")
            return
        context = sys.stdin.read()
        send_to_ai(
            context,
            replace_template_language(COMMAND_OPTION_TO_DESCRIPTION[command], language),
            tmux_pane,
        )
    else:
        print("Invalid command")


if __name__ == "__main__":
    main()
