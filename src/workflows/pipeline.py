from prefect import flow, task
from data.downloader import download_csv
from data.transformer import preprocess_file
from data.writer import write_to_influxdb
from config.loader import load_config
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("workflow", "workflow.log")

@task
def download_data_task():
    """
    Task to download the data using Selenium.
    """
    logger.info("Starting download task...")
    file_path = download_csv()
    logger.info(f"Downloaded file to: {file_path}")
    return file_path

@task
def preprocess_data_task(file_path, config):
    """
    Task to preprocess and validate the data.
    """
    logger.info("Starting data preprocessing task...")
    validated_data = preprocess_file(file_path, config["data_tags"])
    logger.info("Data preprocessing complete.")
    return validated_data

@task
def write_data_task(validated_data, config):
    """
    Task to write validated data to InfluxDB.
    """
    logger.info("Starting data write task...")
    write_to_influxdb(config, validated_data)
    logger.info("Data successfully written to InfluxDB.")

@flow
def data_pipeline():
    """
    Prefect flow to orchestrate the data pipeline.
    """
    logger.info("Starting data pipeline...")
    config = load_config()
    
    # Execute tasks in sequence
    file_path = download_data_task()
    validated_data = preprocess_data_task(file_path, config)
    write_data_task(validated_data, config)

    logger.info("Data pipeline completed successfully.")
