from selenium.webdriver.common.by import By

from helpers import dom
from helpers.dom import DEFAULT_TIMEOUT, ElementCriteriaCondition


def until_visible(driver,
                  selector,
                  selector_type=By.CSS_SELECTOR,
                  timeout=DEFAULT_TIMEOUT):
    """
    Pauses tests until an element that matches the selector is visible.
    Raises an exception if it times out

    :param driver: webdriver
    :param selector: str, CSS selector
    :param selector_type: selector format. Default is By.CSS_SELECTOR
    :param timeout: time to wait before raising exception
    """
    return dom.get_element(
        driver,
        selector,
        selector_type=selector_type,
        timeout=timeout,
        require_single_matching_element=False)


def until_page_title_is(driver, expected_page_title, timeout=DEFAULT_TIMEOUT):
    """
    Pauses tests until the page title matches the expected page title

    :param driver: webdriver
    :param expected_page_title: str, expected page title
    :param timeout: time to wait before raising exception
    """

    def title_filter_function(element):
        page_title = element.get_attribute('textContent')
        return True if page_title == expected_page_title else False

    page_title_condition = ElementCriteriaCondition(
        (By.TAG_NAME, 'title'), must_be_visible=False, filter_function=title_filter_function)

    message = 'Expected page title "{}"'.format(expected_page_title)

    dom.wait_until(driver, page_title_condition, message, timeout)

