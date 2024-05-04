import requests
import time

from src.custom_logger import logger
from src.rpc import fetch_info, fetch_length, update_rp

def get_session_info(session):
    return fetch_info(session), fetch_length(session)

def should_update_rp(info, length, last_info, last_length, last_time):
    return info != last_info or length != last_length or (length['result']['speed'] == 1 and length['result']['time'] != last_time)

def update_and_sleep(info, length, last_info, last_length, last_time):
    if should_update_rp(info, length, last_info, last_length, last_time):
        update_rp(info, length)
        last_info, last_length, last_time = info, length, length['result']['time']
    time.sleep(3)
    return last_info, last_length, last_time

def main():
    try:
        with requests.Session() as session:
            last_info, last_length, last_time = None, None, None
            while True:
                info, length = get_session_info(session)
                if None in (info, length):
                    time.sleep(3)
                    continue
                last_info, last_length, last_time = update_and_sleep(info, length, last_info, last_length, last_time)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    main()