import requests
import time

from src.custom_logger import logger
from src.rpc import fetch_info, fetch_length, update_rp

"""
This file contains the main function of the program. Run this to start the program.
"""

# Main function
def main():
    try:
        with requests.Session() as session:
            last_info, last_length, last_time = None, None, None
            while True:
                info = fetch_info(session)
                length = fetch_length(session)
                if info is None or length is None:  # If either info or length is None, continue to the next iteration
                    time.sleep(3)
                    continue
                if info != last_info or length != last_length or (length['result']['speed'] == 1 and length['result']['time'] == last_time):
                    update_rp(info, length)  # Update the RP if there's new information
                    last_info, last_length, last_time = info, length, last_time  # Update the last info and length
                time.sleep(3)  # Always pause for 3 seconds between iterations
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()