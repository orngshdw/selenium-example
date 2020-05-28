"""
Manages url navigation
"""
def go_to_url(driver, url):
    try:
        driver.get(url)
    except Exception:
        print("Could not navigate to {}".format(url))
        raise

