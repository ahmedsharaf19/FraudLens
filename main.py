from src.app import ConsoleApp
from src.constants import SPACE
import os

if __name__ == "__main__":
    try :
        app = ConsoleApp()
        app.main_menu()
    except:
        print(f"{SPACE}👋 Exiting FRAUDLENS ...")