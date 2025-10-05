BASE_URL = "https://qa-tipalti-assignment.tipalti-pg.com/index.html"
USER_NAME = "Amit Rosen"
USER_EMAIL = "amitrosen4@gmail.com"

MENU_BUTTON_CSS = "a[href='#menu']"
# More specific XPath for menu items - target actual navigation links
MENU_ITEMS_XPATH = "//nav[@id='menu']//a[not(contains(@href, '#menu'))]"
NAME_INPUT_XPATH = "//input[@id='name']"
EMAIL_INPUT_XPATH = "//input[@id='email']"
MESSAGE_INPUT_XPATH = "//textarea[@id='message']"
SUBMIT_BUTTON_XPATH = "//input[@type='submit']"

# Dog names to filter out non-dog menu items
NON_DOG_ITEMS = ['Home', 'Close', 'Menu']
