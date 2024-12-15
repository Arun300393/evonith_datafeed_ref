from utils.logger import setup_logger
import time
import logging

# Setup the logger at the start of the application
setup_logger()

log = logging.getLogger("root")

def retry(retries=3, delay=2, exceptions=(Exception,)):
    """
    A decorator to retry a function execution if it raises an exception.
    
    Args:
        retries (int): Number of retry attempts. Default is 3.
        delay (int): Delay (in seconds) between retries. Default is 2 seconds.
        exceptions (tuple): Tuple of exception types to catch and retry. Default is (Exception,).
    
    Returns:
        Wrapper function with retry logic.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    log.info(f"Attempt {attempts + 1}/{retries} for function '{func.__name__}'")
                    return func(*args, **kwargs)  # Call the original function
                except exceptions as e:
                    attempts += 1
                    log.error(f"Error: {e}. Retrying in {delay} seconds...")
                    if attempts >= retries:
                        log.error(f"Function '{func.__name__}' failed after {retries} retries.")
                        raise  # Re-raise the exception if retries are exhausted
                    time.sleep(delay)  # Wait before retrying
        return wrapper
    return decorator
