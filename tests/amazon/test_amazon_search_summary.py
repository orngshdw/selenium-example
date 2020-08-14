import pytest

from app_data.selectors.amazon import INPUT_SEARCH_BUTTON, INPUT_FIELD, UPPER_RESULT_INFO
from helpers import dom, wait


URL = {
    'link': 'https://www.amazon.com/',
    'title': 'Amazon.com: Online Shopping for Electronics, Apparel, Computers, Books, DVDs & more'
}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_url")
def test_amazon_search_summary(selenium):
    """
    This test validates the expected summary of a search is shown on the search results page.
    """
    search_term = "gardening tools"

    # search for results
    do_search(selenium, search_term)
    # verify results shown for search
    verify_search_result_summary(selenium, expected_prefix='1-48 of over', expected_suffix=search_term)


def do_search(driver, text, enter_to_search=True):
    """
    Enters in a term and then searches by either pressing the enter key or clicking the search button.

    :param driver: selenium webdriver
    :param text: str, text to search for
    :param enter_to_search: bool, do search either with enter key (True) or by clicking the search button (False)
    :return: None
    """
    # format text
    text = "{}{}".format(text, u"\ue007") if enter_to_search else str(text)
    # input value
    dom.set_element_value(driver, INPUT_FIELD, text)

    # if click needed to do search
    if not enter_to_search:
        dom.click_element(driver, INPUT_SEARCH_BUTTON)

    # wait until search results have loaded
    wait.until_visible(driver, UPPER_RESULT_INFO)


def verify_search_result_summary(driver, expected_prefix, expected_suffix):
    """
    Verifies the search summary shown at the top after search results load

    :param driver: selenium webdriver
    :param expected_prefix: str, prefix of the search result summary, such as "1-48 of over"
    :param expected_suffix: str, is the search term user entered to search
    :return: None
    """
    expected_suffix = "\"{}\"".format(expected_suffix)

    # wait until summary result element is visible before getting text
    wait.until_visible(driver, UPPER_RESULT_INFO)
    actual_results_summary = dom.get_elements(driver, UPPER_RESULT_INFO)[0].text

    # validation
    assert expected_prefix == actual_results_summary[:len(expected_prefix)], "Expected\n{}\nbut got\n{}".format(
        expected_prefix, actual_results_summary[:len(expected_prefix)])

    assert expected_suffix == actual_results_summary[-len(expected_suffix):], "Expected\n{}\nbut got\n{}".format(
        expected_suffix, actual_results_summary[-len(expected_suffix):])
