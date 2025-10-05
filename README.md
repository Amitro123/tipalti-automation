# Tipalti Dev-Dogs Automation

This project automates UI testing of the Tipalti Dev-Dogs website, validating menu navigation and contact form submission for each dog profile.

## Requirements
- Python 3.12+
- Google Chrome browser (latest version)
- Dependencies listed in requirements.txt

## Setup

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Chrome is installed and updated** - WebDriver Manager will automatically handle ChromeDriver setup

## Usage

Run the automated tests with:
```bash
pytest test_tipalti_ui.py -v -s
```

**Command flags:**
- `-v`: Verbose output showing test progress
- `-s`: Show print/log statements during test execution

## Project Structure

```
TipaltiTest/
├── test_tipalti_ui.py          # Main test file
├── tipalti_form_filler.py      # Selenium automation class
├── constants.py                # Configuration and selectors
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features

- **Automatic driver management** using WebDriver Manager
- **Dynamic waits** for UI elements to ensure reliability
- **Comprehensive logging** with INFO and DEBUG levels
- **Robust error handling** for flaky elements and async loading
- **Individual dog testing** with detailed progress reporting
- **Graceful failure handling** - continues testing other dogs if one fails

## Test Flow

1. Opens the Tipalti Dev-Dogs website
2. Navigates through the menu to find all dog profiles
3. For each dog:
   - Selects the dog from the menu
   - Fills out the contact form with test data
   - Submits the form
   - Verifies successful submission
4. Reports summary of successful and failed submissions

## Configuration

Edit `constants.py` to modify:
- Base URL
- User credentials for form submission
- CSS/XPath selectors
- Timeout values

## Notes

- Tests are designed to be resilient to timing issues and element loading delays
- Each dog is tested independently - failure of one doesn't stop testing others
- Detailed logging helps with debugging any issues
- The test requires at least one successful dog form submission to pass

## Troubleshooting

**Common issues:**
- **Chrome not found**: Ensure Google Chrome is installed
- **Timeout errors**: Check internet connection and website availability
- **Element not found**: Website structure may have changed - update selectors in constants.py
