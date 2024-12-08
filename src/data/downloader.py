from utils.helper_functions_downloader import clean_folder, rename_file, extract_datetime_from_filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from config.loader import load_config
from pathlib import Path
import os, time
import logging

# Load environment variables
load_dotenv()

# Load config
config = load_config()
log = logging.getLogger("root")
DOWNLOAD_DIR = Path(os.path.abspath(config["selenium"]["download_dir"]))
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
    log.info(f"Downloading to {os.path.abspath(config["selenium"]["download_dir"])}")
    prefs = {
        'profile.default_content_settings.popups': False,
        'download.default_directory': os.path.abspath(config["selenium"]["download_dir"]), #Return a string representation of the path with forward slashes (/)
        'directory_upgrade': True
    }
    options.add_experimental_option('prefs', prefs)

    # Set up WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def download_csv():
    """
    Automates the CSV download by interacting with the webpage using Selenium.
    """
    clean_folder(DOWNLOAD_DIR)
    driver = setup_webdriver()
    try:
        log.info("Opening webpage...")
        driver.get(config["selenium"]["url"])

        # Enter credentials
        username_input = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, "user"))
        )
        username_input.send_keys(USERNAME)

        password_input = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(PASSWORD)

        # Locate and click the download button
        download_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button"))
        )
        log.info("Clicking download button...")
        download_button.click()
        time.sleep(2)
        # Handle potential popup windows
        main_window = driver.current_window_handle
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)
        time.sleep(2)

        log.info("File downloaded successfully.")
        last_csv = sorted(list(filter(lambda x: '.csv' in x, os.listdir(DOWNLOAD_DIR))))[0]
        time_status = extract_datetime_from_filename(last_csv)
        rename_file(last_csv)
        return os.path.join(DOWNLOAD_DIR, "data.csv"), time_status  # Adjust filename if necessary

    except Exception as e:
        log.error(f"Error downloading file: {e}")
        raise

    finally:
        driver.quit()