"""
Amazon specific helpers
"""
from app_data.general.general import ENTER_KEY
from app_data.selectors.amazon import INPUT_FIELD, INPUT_SEARCH_BUTTON, UPPER_RESULT_INFO, RESULTS_CONTAINER
from helpers import dom, wait


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


"""
Verification section
"""
def verify_search_result_summary(driver, expected_prefix, expected_suffix):
    """
    Verifies the search summary shown at the top after search results load

    :param driver: selenium webdriver
    :param expected_prefix: str, prefix of the search result summary, such as "1-48 of over"
    :param expected_suffix: str, is the search term user entered to search
    :return: None
    """
    expected_prefix = '{} '.format(expected_prefix)
    expected_suffix = ' results for "{}"'.format(expected_suffix)

    # wait until results are visible before getting text
    wait.until_visible(driver, RESULTS_CONTAINER)
    actual_results_summary = dom.get_elements(driver, UPPER_RESULT_INFO)[0].text

    # validate prefix and suffix are as expected
    length_prefix, length_suffix = len(expected_prefix), len(expected_suffix)
    assert expected_prefix == actual_results_summary[:length_prefix], \
        "Expected\n{}\nbut got\n{}".format(expected_prefix, actual_results_summary[:length_prefix])
    assert expected_suffix == actual_results_summary[-length_suffix:], \
        "Expected\n{}\nbut got\n{}".format(expected_suffix, actual_results_summary[-length_suffix:])
