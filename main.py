import requests
import time
from src.custom_logger import logger
from src.rpc import KodiRPC

KodiRPC = KodiRPC()

class KodiMonitor:
    def __init__(self):
        self.last_info = None
        self.last_length = None
        self.last_time = None
        self.session = requests.Session()

    def run(self):
        try:
            while True:
                info = KodiRPC.fetch_info()
                length = KodiRPC.fetch_length()
                if info is None or length is None:  # If either info or length is None, continue to the next iteration
                    time.sleep(3)
                    continue
                if info != self.last_info or length != self.last_length or (length['result']['speed'] == 1 and length['result']['time'] == self.last_time):
                    KodiRPC.update_rp(self, info, length)  # Update the RP if there's new information
                    self.last_info, self.last_length, self.last_time = info, length, length['result']['time']  # Update the last info and length
                time.sleep(3)  # Always pause for 3 seconds between iterations
        except KeyboardInterrupt:
            logger.info("Program interrupted by user. Exiting...")

if __name__ == "__main__":
    monitor = KodiMonitor()
    monitor.run()