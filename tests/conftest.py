"""
Fixtures that setup state of site before executing tests.

Code such as logging in and accessing webpages that are likely to be
repetitive in all tests are great candidates for turning in a fixture.
"""
import pytest

from helpers import dom, url, wait


@pytest.fixture(scope='function')
def open_url(request, selenium):
    """
    Navigates to a webpage defined as a global dict.

    The name of the global dict should be defined in the test module before
    the test function and follow the below example:
        URL = {
            'link': 'url link',
            'title': 'url page title'
            'pop-up': 'css'
        }
    """
    url_info = getattr(request.module, 'URL')
    url.go_to_url(selenium, url_info['link'])
    wait.until_page_title_is(selenium, url_info['title'])

    # close any pop-ups that appear after navigating to page
    if 'pop-up' in url_info:
        wait.until_visible(selenium, url_info['pop-up'])
        dom.click_element(selenium, url_info['pop-up'])
