"""
Class to fill out the Tipalti Dev-Dogs Foundation contact form
"""
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from constants import (MENU_BUTTON_CSS, MENU_ITEMS_XPATH, NAME_INPUT_XPATH, EMAIL_INPUT_XPATH,
                       MESSAGE_INPUT_XPATH, SUBMIT_BUTTON_XPATH, NON_DOG_ITEMS)

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)


class TipaltiFormFiller:
    def __init__(self, timeout=20):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        logger.info("Initializing Chrome WebDriver with WebDriver Manager")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, timeout)
        logger.info(f"WebDriver initialized with {timeout}s timeout")

    def open_site(self, url):
        try:
            logger.info(f"Opening site: {url}")
            self.driver.get(url)
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(),'The Tipalti Dev-Dogs Foundation')]")
                )
            )
            logger.info("Site loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to open site {url}: {e}")
            return False

    def open_menu(self):
        try:
            logger.debug("Clicking menu button")
            menu_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MENU_BUTTON_CSS)))
            menu_button.click()
            
            logger.debug("Waiting for menu items to load")
            self.wait.until(lambda driver: len(self.get_menu_items()) >= 3)
            logger.info("Menu opened successfully")
            return True
        except TimeoutException:
            logger.error(f"Menu button not found or menu items not fully loaded: {MENU_BUTTON_CSS}")
            return False
        except Exception as e:
            logger.error(f"Error in open_menu: {e}")
            return False

    def get_menu_items(self):
        try:
            menu_items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, MENU_ITEMS_XPATH)))
            items = []
            for item in menu_items:
                text = item.text.strip()
                if text and text not in NON_DOG_ITEMS:
                    items.append(text)
            logger.debug(f"Found dog menu items: {items}")
            return items
        except TimeoutException:
            logger.error(f"Menu items not found: {MENU_ITEMS_XPATH}")
            return []

    def select_menu_item(self, dog_name):
        try:
            logger.debug(f"Selecting menu item: {dog_name}")
            menu_items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, MENU_ITEMS_XPATH)))
            for item in menu_items:
                if item.text.strip() == dog_name:
                    logger.debug(f"Found menu item for {dog_name}, scrolling into view")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space(text())='{dog_name}']")))
                    item.click()
                    logger.info(f"Successfully selected menu item: {dog_name}")
                    return True
            logger.warning(f"Menu item '{dog_name}' not found")
            return False
        except Exception as e:
            logger.error(f"Failed to select menu item '{dog_name}': {e}")
            return False

    def fill_contact_form(self, name, email, message):
        try:
            logger.debug("Locating form elements")
            name_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, NAME_INPUT_XPATH)))
            email_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, EMAIL_INPUT_XPATH)))
            message_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, MESSAGE_INPUT_XPATH)))
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, SUBMIT_BUTTON_XPATH)))

            logger.debug("Filling form fields")
            name_input.clear()
            name_input.send_keys(name)

            email_input.clear()
            email_input.send_keys(email)

            message_input.clear()
            message_input.send_keys(message)

            logger.debug("Submitting form")
            submit_button.click()
            logger.info("Contact form submitted successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to fill contact form: {e}")
            return False

    def close(self):
        try:
            logger.info("Closing browser")
            self.driver.quit()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
