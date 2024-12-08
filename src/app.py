from utils.logger import setup_logger
from workflows.pipeline import data_pipeline
import logging

# Setup the logger at the start of the application
setup_logger()

log = logging.getLogger("root")

if __name__ == "__main__":
    log.info("Starting the data pipeline")
    data_pipeline()