selenium_skeleton
------

# Setup Instructions
Using python3 install the `requirements-to-freeze.txt` file:
```bash
pip install -r requirements-to-freeze.txt
```

# Run Tests
There are 2 options available to run the tests via the terminal.
## Showing browser window
This option will run tests after launching a Chrome browser. Useful for seeing tests run.
```bash
pytest --driver Chrome -vv
```
The `-vv` flag is optional but will make pytest verbose and show status of the individual tests ran.
## Headless (no browser window)
This option will run tests in the background using the headless Chrome browser.
```bash
pytest --headless --driver Chrome -vv
```
# Additional Information
Tested with latest `ChromeDriver 73.0.3683.68 (47787ec04b6e38e22703e856e101e840b65afe72)`
