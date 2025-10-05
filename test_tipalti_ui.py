import logging
import pytest
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tipalti_form_filler import TipaltiFormFiller
from constants import BASE_URL, USER_NAME, USER_EMAIL

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


@pytest.fixture
def form_filler():
    ff = TipaltiFormFiller()
    yield ff
    ff.close()


def test_dog_menu_options(form_filler):
    """Test that all dog menu options are accessible and have working contact forms."""
    logger.info("Starting dog menu options test")
    
    form_filler.open_site(BASE_URL)
    form_filler.open_menu()

    menu_items = form_filler.get_menu_items()
    assert len(menu_items) > 0, "No dog menu items found"
    logger.info(f"Found {len(menu_items)} dog menu items: {menu_items}")

    successful_submissions = 0
    failed_dogs = []

    for i, dog_name in enumerate(menu_items):
        logger.info(f"Testing dog {i+1}/{len(menu_items)}: {dog_name}")
        try:
            # Navigate back to base URL
            logger.debug(f"Opening site: {BASE_URL}")
            if not form_filler.open_site(BASE_URL):
                failed_dogs.append(f"{dog_name}: Failed to open site")
                continue
            
            # Brief wait for page stabilization
            time.sleep(1)

            # Open menu
            logger.debug("Opening menu...")
            if not form_filler.open_menu():
                failed_dogs.append(f"{dog_name}: Failed to open menu")
                continue

            # Debug: Check what menu items are available now
            current_menu_items = form_filler.get_menu_items()
            logger.debug(f"Current menu items: {current_menu_items}")
            
            if dog_name not in current_menu_items:
                failed_dogs.append(f"{dog_name}: Dog not found in current menu items {current_menu_items}")
                continue

            # Select the dog
            logger.debug(f"Selecting dog: {dog_name}")
            if not form_filler.select_menu_item(dog_name):
                failed_dogs.append(f"{dog_name}: Failed to select menu item")
                continue

            # Wait for page transition and log URL
            wait = WebDriverWait(form_filler.driver, 10)
            wait.until(lambda driver: driver.current_url != BASE_URL)
            current_url = form_filler.driver.current_url
            logger.debug(f"Current URL after selection: {current_url}")

            # Create unique message
            unique_message = f"Test message for {dog_name} - {int(time.time())}"
            logger.debug("Filling contact form...")

            # Fill contact form
            if not form_filler.fill_contact_form(USER_NAME, USER_EMAIL, unique_message):
                failed_dogs.append(f"{dog_name}: Failed to fill contact form")
                continue

            # Wait for form submission to complete
            time.sleep(2)

            # Check if form was submitted successfully
            final_url = form_filler.driver.current_url
            logger.debug(f"Final URL: {final_url}")
            
            if final_url == BASE_URL:
                failed_dogs.append(f"{dog_name}: Form submission failed - still on base URL")
                continue

            successful_submissions += 1
            logger.info(f"✓ Successfully submitted form for {dog_name}")

        except (TimeoutException, NoSuchElementException) as e:
            failed_dogs.append(f"{dog_name}: Element not found - {str(e)}")
            logger.error(f"Failed to find elements for {dog_name}: {e}")

        except AssertionError as e:
            failed_dogs.append(f"{dog_name}: Assertion failed - {str(e)}")
            logger.error(f"Assertion failed for {dog_name}: {e}")

        except Exception as e:
            failed_dogs.append(f"{dog_name}: Unexpected error - {str(e)}")
            logger.error(f"Unexpected error for {dog_name}: {e}")

    # Final test results
    logger.info("=== Test Summary ===")
    logger.info(f"Total dogs tested: {len(menu_items)}")
    logger.info(f"Successful submissions: {successful_submissions}")
    logger.info(f"Failed submissions: {len(failed_dogs)}")

    if failed_dogs:
        logger.warning("Failed dogs:")
        for failure in failed_dogs:
            logger.warning(f"  - {failure}")

    assert successful_submissions > 0, f"No dogs had working forms. Failures: {failed_dogs}"
    logger.info("Test completed successfully")
