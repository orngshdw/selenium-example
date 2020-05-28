"""
Fixtures that setup state of site before executing tests.

Code such as logging in and accessing webpages that are likely to be
repetitive in all tests are great candidates for turning in a fixture.
"""
import pytest

from helpers import dom, url, wait
from helpers.authentication import login


@pytest.fixture(scope='function')
def open_url(request, selenium):
    """
    Navigates to a webpage defined as a global dict.

    The name of the global dict should be defined in the test module before
    the test function and follow the below example:
        URL = {
            'link': 'url link',
            'title': 'url page title'
        }
    """
    url_info = getattr(request.module, 'URL')
    url.go_to_url(selenium, url_info['link'])
    wait.until_page_title_is(selenium, url_info['title'])


@pytest.fixture(scope='function')
def join_as_individual(request, selenium):
    """
    Access registration page

    :param request: pytest fixture containing test metadata
    :param selenium: pytest-selenium fixture
    """
    url_link = getattr(request.module, 'url_link', None)
    url.go_to_url(selenium, url_link)
    wait.until_page_title_is(selenium, None)
    dom.click_element(selenium, "button", text="JOIN AS AN INDIVIDUAL")


@pytest.fixture(scope='function')
def new_search_talent(request, selenium):
    """
    Login and then clicks the "Find Talent" link. Default login credentials are:

        test_username = "qa tester"
        test_password = "testerpassword"

    :param request: pytest fixture containing test metadata
    :param selenium: pytest-selenium fixture
    """
    test_username = getattr(request.module, 'test_username', None)
    test_password = getattr(request.module, 'test_password', None)

    login(selenium, test_username, test_password)
    dom.click_element(selenium, "[href='/search/']")

