"""
Test talent search results to determine if each card contains search term "test".
"""
import pytest

from app_data.selectors.talent_search import SEARCH_FIELD, VENDOR_CARD, PROFILE_DETAILS
from helpers import dom, wait


@pytest.mark.usefixtures("new_search_talent")
def test_talent_search(selenium):
    """
    Searches for profile cards that contain the word "test".
    Gets text from each profile card on the first page of the returned results.
    Verifies each card contains the searched term.

    :param selenium: selenium webdriver, specified by pytest flags
    """

    search_term = "test"
    ENTER_KEY = u"\ue007"
    results_per_page = 50

    # type in "test" to search field and presses Enter key
    dom.set_element_value(selenium, SEARCH_FIELD, search_term + ENTER_KEY)
    # wait until a vendor card is visible before proceeding
    wait.until_visible(selenium, VENDOR_CARD)

    # get all profile elements on page
    profile_card_details = dom.get_elements(selenium, PROFILE_DETAILS)
    # set up list to record incorrect matches
    false_count, false_card_returns = 0, []
    # confirm text profile cards contains the search term
    for n in range(results_per_page):
        card = profile_card_details[n].text
        # if the search term is not present in a card, record the incorrect card
        if search_term not in card.lower():
            false_count += 1
            false_card_returns.append(card)

    # fail the test if any incorrect cards were found. Prints data about each incorrect card
    assert not false_count, "Search '{}' returned {} incorrect profile cards:\n{}"\
        .format(search_term, false_count, false_card_returns)

