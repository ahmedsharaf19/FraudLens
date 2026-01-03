import os
import shutil
from src.constants import banner, SPACE

def clear_screen():
    """Clear the terminal screen (Windows command)."""
    os.system('cls')

def print_centered(text: str):
    """Print text centered in the terminal width."""
    width = shutil.get_terminal_size((80, 20)).columns
    for line in text.splitlines():
        print(line.center(width))

def show_banner():
    """Display the application banner centered in the terminal."""
    print_centered(banner)

def wait():
    """Block until the user presses Enter."""
    input(f"\n{SPACE}🔹 Press Enter to continue...")

def error(msg: str):
    """Display an error message and wait for user acknowledgement."""
    show_banner()
    print(f"\n{SPACE}❌ {msg}")
    wait()