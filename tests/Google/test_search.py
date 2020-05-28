import pytest

from app_data.selectors.google_selectors import INPUT_FIELD, NAVIGATION_PAGES, RESULT_STATS
from helpers import dom, wait


URL = {
    'link': 'https://www.google.com/',
    'title': 'Google'
}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_url")
def test_search(selenium):
    """
    This test validates:
        1. search page loads after entering search
        2. users can view second page of results
    """
    search_term = "cat pictures"
    ENTER_KEY = u"\ue007"

    # search for results
    dom.set_element_value(selenium, INPUT_FIELD, search_term+ENTER_KEY)
    # wait until search results have loaded
    wait.until_visible(selenium, RESULT_STATS)

    # click to view second page of search results
    dom.click_element(selenium, NAVIGATION_PAGES.format("2"))

    # validate second page loads and is showing stats
    wait.until_visible(selenium, RESULT_STATS)
    verify_prefix(selenium, RESULT_STATS, 'Page 2 of about')


def verify_prefix(driver, selector, expected_text):
    element_with_text = dom.get_element(driver, selector)
    assert element_with_text.text[:15] == expected_text
