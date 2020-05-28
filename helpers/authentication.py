"""
Contain login actions
"""
from app_data.selectors.authentication import USERNAME_INPUT, PASSWORD_INPUT, \
    LOGIN_BUTTON
from helpers import dom, url, wait

# login page url
HOST = "http://www.basesite.com/"
LOGIN_URL = "{}login".format(HOST)


def login(driver, uname='test', pword='test'):
    """
    Log into site with provided information

    :param driver: webdriver
    :param uname: str, username
    :param pword: str, password
    """
    url.go_to_url(driver, LOGIN_URL)
    wait.until_page_title_is(driver, 'Login page name')

    dom.set_element_value(driver, USERNAME_INPUT, uname)
    dom.set_element_value(driver, PASSWORD_INPUT, pword)
    dom.click_element(driver, LOGIN_BUTTON)
    wait.until_page_title_is(driver, 'Logged in page name')

