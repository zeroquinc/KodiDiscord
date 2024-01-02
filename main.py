import requests
import logging
from rpc import fetch_info, fetch_length, update_rp

def main():
    try:
        with requests.Session() as session:
            while True:
                info = fetch_info(session)
                length = fetch_length(session)
                if info is not None and length is not None:
                    update_rp(info, length)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()