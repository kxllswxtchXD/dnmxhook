import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))
from modules.clear import clear
from modules.temp import temp
from modules.login import login
from modules.cleanup import cleanup

def main():
    clear()
    temp()
    login()
    cleanup()
if __name__ == "__main__":
    main()