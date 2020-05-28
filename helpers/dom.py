"""
Contains non application specific & low-level actions used by tests
"""
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# set timeout
DEFAULT_TIMEOUT = 60


def get_element(driver,
                selector,
                text='',
                selector_type=By.CSS_SELECTOR,
                timeout=DEFAULT_TIMEOUT,
                must_be_visible=True,
                require_single_matching_element=True,
                action_callback=None):
    """
    Pauses execution until an element matching the selector is visible.

    :param driver: webdriver
    :param selector: str, CSS selector
    :param text: text that the element should contain
    :param selector_type: selector format. Default is By.CSS_SELECTOR
    :param timeout: int, time to wait before raising exception
    :param must_be_visible: bool, true if the returned components must be visible
    :param require_single_matching_element: bool, raise WebException if >1 element matches criteria
    :param action_callback: function, a function called on the matched element
        If this function throws an exception (e.g. a StaleElementException), will retry until timeout
    :return: the matched element.
    """
    callback = ElementCriteriaCondition(
        (selector_type, selector),
        text,
        must_be_visible=must_be_visible,
        require_single_matching_element=require_single_matching_element,
        action_callback=action_callback)
    message = 'No element matching {} `{}` was found'.format(selector_type,
                                                             selector)
    if text:
        message += ' containing text `{}`'.format(text)

    try:
        return wait_until(driver, callback, message, timeout)
    except TimeoutException as e:
        raise WebException(e.msg) from e


def get_elements(driver,
                 selector,
                 text='',
                 selector_type=By.CSS_SELECTOR,
                 timeout=DEFAULT_TIMEOUT,
                 must_be_visible=True):
    """
    Pauses execution until one or more elements matching the selector is visible.

    :param driver: webdriver
    :param selector: str, CSS selector
    :param text: text that the element should contain
    :param selector_type: selector format. Default is By.CSS_SELECTOR
    :param timeout: int, time to wait before raising exception
    :param must_be_visible: bool, true if the returned components must be visible
    :return: the matched element
    """
    callback = ElementCriteriaCondition(
        (selector_type, selector),
        text,
        must_be_visible=must_be_visible,
        return_all_matching=True)
    message = "Expected at least one element matching {} `{}` to become " \
              "visible".format(selector_type, selector)
    if text:
        message += ' containing text `{}`'.format(text)

    try:
        return wait_until(driver, callback, message, timeout)
    except TimeoutException as e:
        raise WebException(e.msg) from e


def wait_until(driver, callback, message='', timeout=DEFAULT_TIMEOUT):
    """
    Blocks execution until condition returned by callback is not false
    See selenium.webdriver.support.wait.WebDriverWait
    """
    return WebDriverWait(driver, timeout).until(callback, message)


def click_element(driver,
                  selector,
                  text='',
                  selector_type=By.CSS_SELECTOR,
                  timeout=DEFAULT_TIMEOUT,
                  must_be_visible=True):
    """
    Pauses execution until element that matches the specified selector is visible.
    Then clicks the element.

    :param driver: webdriver
    :param selector: str, CSS selector
    :param text: text that the element should contain
    :param selector_type: selector format. Default is By.CSS_SELECTOR
    :param timeout: int, time to wait before raising exception
    :param must_be_visible: bool, true if the returned components must be visible
    :return: the clicked element
    """
    def click_element_action_callback(found_element):
        found_element.click()

    element = get_element(
        driver,
        selector,
        text,
        selector_type,
        timeout,
        must_be_visible=must_be_visible,
        action_callback=click_element_action_callback)
    return element


def set_element_value(driver,
                      selector,
                      value,
                      text='',
                      selector_type=By.CSS_SELECTOR,
                      timeout=DEFAULT_TIMEOUT):
    """
    Pause execution until an element matching the selector is visible.
    After, the element is cleared and the value is sent to the element.

    :param driver: webdriver
    :param selector: str, CSS selector
    :param value: str, value to send to the element
    :param text: text that the element should contain
    :param selector_type: selector format. Default is By.CSS_SELECTOR
    :param timeout: int, time to wait before raising exception
    :return: the element
    """
    element = click_element(driver, selector, text, selector_type, timeout)
    # Open Selenium issue with clearing fields so am not using element.clear()
    # Issue: https://github.com/SeleniumHQ/selenium/issues/1841
    # element.clear()
    driver.execute_script('arguments[0].value="";', element)
    element.send_keys(value)
    return element


class ElementCriteriaCondition(object):
    """
    An expectation as per
    selenium.webdriver.support.expected_conditions
    that finds all visible elements matching the selector and elements with expected text
    content. If >1 element found, an Exception is raise, else the matched element is returned
    """

    def __init__(self,
                 locator,
                 text='',
                 must_be_visible=True,
                 return_all_matching=False,
                 filter_function=None,
                 require_single_matching_element=True,
                 action_callback=None):
        """
        ElementCriteriaCondition desired conditions.

        :param locator: tuple, (selector_type, selector)
        :param text: str, text that the element should contain
        :param must_be_visible: boolean, True if the element must be visible
        :param filter_function: function, takes an element as a parameter and
                                returns boolean True if the element matches criteria (else False)
        :param action_callback: function, used on elements found
        """
        self.locator = locator
        self.text = text
        self.return_all_matching = return_all_matching
        self.require_single_matching_element = require_single_matching_element
        self.action_callback = action_callback

        self.test_element = lambda element: (
                (not text or (text in element.text))
                and (not must_be_visible or element.is_displayed())
                and (not filter_function or filter_function(element))
        )

    def __call__(self, driver):
        try:
            found_elements = driver.find_elements(*self.locator)
            element_generator = (element for element in found_elements if self.test_element(element))
            if self.return_all_matching:
                result = list(element_generator)
            else:
                result = next(element_generator, None)

                # If more than 1 match raise an exception
                if self.require_single_matching_element and next(element_generator, None):
                    msg = "Found more than one element for {} `{}`".format(*self.locator)
                    if self.text:
                        msg += " with text `{}`".format(self.text)
                    msg += ". Please make the selector more specific, set the error_if_selector_matches_many_elements" \
                           " flag to False or consider using dom.get_elements"
                    raise WebException(msg)

            if result and self.action_callback:
                self.action_callback(result)
            return result

        except (StaleElementReferenceException, WebDriverException, StopIteration):
            return False


class WebException(Exception):
    """
    Custom exception for this web test framework
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

