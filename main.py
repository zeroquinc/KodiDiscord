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
            last_data = None
            while True:
                current_data = (fetch_info(session), fetch_length(session))
                if None not in current_data: # Check if info and length are not None because if they are, it means Kodi is not playing anything
                    if current_data != last_data:
                        update_rp(*current_data) # Update the RP if there's new information
                        last_data = current_data # Update the last info and length
                    else:
                        time.sleep(3)  # Pause for 3 seconds if there's no new information
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()