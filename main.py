import requests
import logging
import time
from rpc import fetch_info, fetch_length, update_rp

def main():
    try:
        with requests.Session() as session:
            last_info, last_length = None, None
            while True:
                info = fetch_info(session)
                length = fetch_length(session)
                logging.debug(f"Fetched info: {info}")
                logging.debug(f"Fetched length: {length}")
                if info is not None and length is not None:
                    if info != last_info or length != last_length:
                        update_rp(info, length)
                        last_info, last_length = info, length
                    else:
                        time.sleep(1)  # Pause for 1 second if there's no new information
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()