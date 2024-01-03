import requests
import time
from rpc import fetch_info, fetch_length, update_rp
from logging import get_logger

logger = get_logger(__name__)

def main():
    try:
        with requests.Session() as session:
            last_info, last_length = None, None
            while True:
                info = fetch_info(session)
                length = fetch_length(session)
                logger.debug(f"Fetched info: {info}")
                logger.debug(f"Fetched length: {length}")
                if info is not None and length is not None:
                    if info != last_info or length != last_length:
                        update_rp(info, length)
                        last_info, last_length = info, length
                    else:
                        time.sleep(1)  # Pause for 1 second if there's no new information
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()