import logging
import os


def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/acquisition.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("AAG")


logger = setup_logger()
