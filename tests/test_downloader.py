import pytest
from unittest.mock import patch, MagicMock
from data.downloader import setup_webdriver, download_csv

@patch("data.downloader.webdriver.Chrome")
@patch("data.downloader.WebDriverWait")
def test_download_csv(mock_wait, mock_chrome):
    # Mock Chrome WebDriver instance
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver

    # Mock WebDriverWait behavior
    mock_wait.return_value.until.return_value = MagicMock()

    # Mock file download
    mock_driver.current_window_handle = "main_window"
    mock_driver.window_handles = ["main_window"]
    mock_driver.get.return_value = None

    # Call the function
    with patch("os.path.join", return_value="mocked_path.xlsx"):
        downloaded_file = download_csv()

    # Assertions
    mock_driver.get.assert_called_once_with("https://mcartalert.com/WebService/GeneralService.asmx?op=realtimedataVP")
    assert downloaded_file == "mocked_path.xlsx"
