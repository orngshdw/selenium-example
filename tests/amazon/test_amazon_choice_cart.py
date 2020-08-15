import pytest

from app_data.selectors.amazon import AMAZON_CHOICE, PRODUCT_TITLE
from helpers import dom
from helpers.amazon import do_search, add_to_cart, go_to_cart, verify_items_in_cart

URL = {
    'link': 'https://www.amazon.com/',
    'title': 'Amazon.com: Online Shopping for Electronics, Apparel, Computers, Books, DVDs & more'
}


@pytest.mark.usefixtures("open_url")
@pytest.mark.parametrize("search_term", ("teacups",))
def test_amazon_search_summary(selenium, search_term):
    """
    This test validates adding an "Amazon's Choice" item to the cart shows up in the cart list.
    """
    # search for results
    do_search(selenium, search_term)

    # add Amazon's Choice pick to cart
    dom.click_element(selenium, AMAZON_CHOICE)
    product_name = dom.get_element(selenium, PRODUCT_TITLE).text
    add_to_cart(selenium)

    # verify added item in cart
    go_to_cart(selenium)
    verify_items_in_cart(selenium, product_name)
