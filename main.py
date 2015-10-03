from retrogamelib import display
from retrogamelib.constants import *
from retrogamelib import button
import menu


def main():
    display.init(3.0, "Spinner",  GBRES)
    menu.run_menu()
    # while True:
    #     button.handle_input()
    #     # if input():
    #     #     break;
