import time

"""
This file contains utility functions that are used in the program.
"""

def loading(string):
    for x in range(0, 6):
        b = string + "." * x
        print(b, end="\r")
        time.sleep(1)