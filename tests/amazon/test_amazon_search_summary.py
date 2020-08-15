import pytest

from app_data.selectors.amazon import NEXT_BUTTON
from helpers import dom
from helpers.amazon import do_search, verify_search_result_summary

URL = {
    'link': 'https://www.amazon.com/',
    'title': 'Amazon.com: Online Shopping for Electronics, Apparel, Computers, Books, DVDs & more'
}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_url")
@pytest.mark.parametrize("search_term", ("gardening tools", "plush animals", "pots",))
def test_amazon_search_summary(selenium, search_term):
    """
    This test validates the expected summary of a search is shown on the first and second search results page.
    Search terms used are defined in the parameterize pytest marker above.
    """
    # search for results
    do_search(selenium, search_term)
    # verify results shown for search
    verify_search_result_summary(selenium, low=1, high=48, expected_search_term=search_term)

    dom.click_element(selenium, NEXT_BUTTON)
    verify_search_result_summary(selenium, low=49, high=96, expected_search_term=search_term)
