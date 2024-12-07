import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from config.loader import load_config
from utils.logger import setup_logger
from utils.helper_functions_downloader import remove_csv, rename_csv

# Load environment variables
load_dotenv()

# Load config
config = load_config()
DOWNLOAD_DIR = os.path.abspath(config["selenium"]["download_dir"])
USERNAME = os.getenv("USERNAME_REALTIMEDATA")
PASSWORD = os.getenv("PASSWORD_REALTIMEDATA")

def setup_webdriver():
    """
    Sets up the Chrome WebDriver with dynamic download directory.
    Returns:
        WebDriver: Configured Chrome WebDriver instance.
    """
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {
        'profile.default_content_settings.popups': False,
        'download.default_directory': DOWNLOAD_DIR,
        'directory_upgrade': True
    }
    options.add_experimental_option('prefs', prefs)

    # Set up WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Setup logger
logger = setup_logger("downloader", "downloader.log")

def download_csv():
    """
    Automates the CSV download by interacting with the webpage using Selenium.
    """
    driver = setup_webdriver()
    try:
        logger.info("Opening webpage...")
        driver.get(config["selenium"]["url"])

        # Enter credentials
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "user"))
        )
        username_input.send_keys(USERNAME)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(PASSWORD)

        # Locate and click the download button
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button"))
        )
        logger.info("Clicking download button...")
        download_button.click()

        # Handle potential popup windows
        main_window = driver.current_window_handle
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)

        logger.info("File downloaded successfully.")
        last_csv = sorted(list(filter(lambda x: '.csv' in x, os.listdir(DOWNLOAD_DIR))))[-1]
        rename_csv(last_csv)
        remove_csv()
        return os.path.join(DOWNLOAD_DIR, "data.xlsx")  # Adjust filename if necessary

    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise

    finally:
        driver.quit()
