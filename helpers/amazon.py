"""
Amazon specific helpers
"""
from selenium.common.exceptions import StaleElementReferenceException

from app_data.general.general import ENTER_KEY
from app_data.selectors.amazon import INPUT_FIELD, INPUT_SEARCH_BUTTON, UPPER_RESULT_INFO, RESULTS_CONTAINER, \
    ADD_TO_CART_BUTTON, PRODUCT_TITLE, VIEW_CART_BUTTON, CART_PRODUCT_TITLE
from helpers import dom, wait
from helpers.dom import WebException

"""
Test workflow/actions section
"""
def do_search(driver, text, enter_to_search=True):
    """
    Enters in a term and then searches by either pressing the enter key or clicking the search button.

    :param driver: selenium webdriver
    :param text: str, text to search for
    :param enter_to_search: bool, do search either with enter key (True) or by clicking the search button (False)
    :return: None
    """
    # format text
    text = "{}{}".format(text, ENTER_KEY) if enter_to_search else str(text)
    # input value
    dom.set_element_value(driver, INPUT_FIELD, text)

    # if click needed to do search
    if not enter_to_search:
        dom.click_element(driver, INPUT_SEARCH_BUTTON)

    # wait until search results have loaded
    wait.until_visible(driver, UPPER_RESULT_INFO)

def add_to_cart(driver):
    """
    Clicks the "Add to Cart" button on a product page

    :param driver: selenium webdriver
    :return: None
    """
    wait.until_visible(driver, PRODUCT_TITLE)
    wait.until_visible(driver, ADD_TO_CART_BUTTON)
    dom.click_element(driver, ADD_TO_CART_BUTTON)


def go_to_cart(driver):
    """
    Clicks any visible button that will navigate to the show the cart list page

    :param driver: selenium webdriver
    :return: None
    """
    view_cart_buttons = iter(dom.get_elements(driver, VIEW_CART_BUTTON))
    button = next(view_cart_buttons)
    while button:
        try:
            button.click()
            return
        except (StaleElementReferenceException, ValueError):
            button = next(view_cart_buttons)

    raise WebException("No button to go to cart visible.")


"""
Verification section
"""
def verify_items_in_cart(driver, *expected_names):
    """
    Verifies the provided product names are listed in the cart.

    :param driver: selenium webdriver
    :param expected_names: str, expected product names to be in cart
    :return: None
    """
    products_in_cart = {item.text for item in dom.get_elements(driver, CART_PRODUCT_TITLE)}
    missing_items = set(expected_names).difference(products_in_cart)
    assert not missing_items, "The following items are missing from the cart:\n{}".format(missing_items)


def verify_search_result_summary(driver, low, high, expected_search_term):
    """
    Verifies the search summary shown at the top after search results load

    :param driver: selenium webdriver
    :param expected_prefix: str, prefix of the search result summary, such as "1-48 of over"
    :param expected_suffix: str, is the search term user entered to search
    :return: None
    expected_prefix = '{} '.format(expected_prefix)
    expected_suffix = ' results for "{}"'.format(expected_suffix)

    """
    # wait until results are visible before getting text
    wait.until_visible(driver, RESULTS_CONTAINER)

    # will look something like ['1-48 of over 30,000 results for ', 'gardening tools', '']
    actual_results_summary = dom.get_elements(driver, UPPER_RESULT_INFO)[0].text.split('"')
    actual_search_term = actual_results_summary[1]
    assert expected_search_term == actual_search_term, \
        "Expected search term `{}`, but got `{}` in search results summary:\n{}".format(expected_search_term,
                                                                                        actual_search_term,
                                                                                        actual_results_summary)

    actual_results_summary_prefix = actual_results_summary[0].split(' ')
    expected_results_summary_prefix = ['{}-{}'.format(low, high), 'of', 'over', '<number>', 'results', 'for', '']
    for i, actual_word in enumerate(actual_results_summary_prefix):
        if i == 3:
            int(actual_word.replace(',', ''))
            continue
        assert expected_results_summary_prefix[i] == actual_word, \
            "Expected `{}` but got `{}` in the summary:\n{}".format(expected_results_summary_prefix[i],
                                                                    actual_word, actual_results_summary_prefix)


