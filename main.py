import requests
import logging
from rpc import fetch_info, fetch_length, update_rp

# Define the main function
def main():
    try:
        # Create a session using the requests library
        with requests.Session() as session:
            # Continuously fetch information and update the Rich Presence
            while True:
                # Fetch information about the current media from the session
                info = fetch_info(session)
                # Fetch the length of the current media from the session
                length = fetch_length(session)
                # If both info and length are not None, update the Rich Presence
                if info is not None and length is not None:
                    update_rp(info, length)
    # If the user interrupts the program, log an info message and exit
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")

# If this script is run directly (not imported as a module), call the main function
if __name__ == "__main__":
    main()