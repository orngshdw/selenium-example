"""
Tests the registration form for individual registration
"""
import pytest
import random
import string
import time

from app_data.selectors.signup_page import FIRSTNAME, LASTNAME, EMAIL, PASSWORD, REGISTER_BTN, CHECKBOX, \
    PWD_WARNING
from helpers import dom, wait

# Registration url
url_link = None


@pytest.mark.usefixtures("join_as_individual")
def test_registration_base_case(selenium):
    """
    Fills in the individual registration form.
    Confirms the "REGISTER" button is inactive until all fields are completed correctly
    Clicks REGISTER button
    Confirms successful registration page is loaded

    :param selenium: selenium webdriver, specified by pytest flags
    """
    first_name = random_letter_generator()
    last_name = random_letter_generator()
    register_fields = {
        FIRSTNAME: first_name,
        LASTNAME: last_name,
        EMAIL: first_name + last_name + "@gmail.com",
        PASSWORD: random_letter_generator() + "123"
    }
    # get REGISTER button
    register_button = dom.get_element(selenium, REGISTER_BTN)

    # make sure register button is initially inactive
    assert not register_button.is_enabled()

    # check agreement checkbox
    dom.click_element(selenium, CHECKBOX, must_be_visible=False)
    assert not register_button.is_enabled()

    # fill in fields and check register button is inactivated until last field is complete
    filled_fields = 0
    for field, text in register_fields.items():
        dom.set_element_value(selenium, field, text)
        filled_fields += 1
        # unless the last field is filled, confirm REGISTER button is not clickable
        if filled_fields < len(register_fields):
            assert not register_button.is_enabled()

    # confirm register button is clickable
    assert register_button.is_enabled()

    # click REGISTER button
    register_button.click()
    # wait for Thank you page to load
    wait.until_page_title_is(selenium, None)


@pytest.mark.usefixtures("join_as_individual")
def test_registration_simple_password(selenium):
    """
    Fills in registration form using a very simple password
    Confirms warning about password being too simple exists

    :param selenium: selenium webdriver, specified by pytest flags
    """
    # Warning message expected by site
    expected_warning = "Your password entered is not allowed because it is too simple"
    # generate random first/last names
    first_name = random_letter_generator()
    last_name = random_letter_generator()

    # fill out the individual registration form
    fill_individual_form(selenium, first_name, last_name,
                         first_name + last_name + "@gmail.com",
                         "Password1", checkbox=True)

    # click REGISTER button to trigger password warning
    dom.click_element(selenium, REGISTER_BTN)

    # wait for password warning to appear
    warning = wait.until_visible(selenium, PWD_WARNING)

    # confirm expected warning message is displayed
    assert warning.text == expected_warning, "Warning message read {}, expected {}".format(warning.text, expected_warning)


@pytest.mark.usefixtures("join_as_individual")
def test_emails(selenium):
    """
    Edge case test to confirm REGISTER button is active and clickable only when valid emails are entered

    :param selenium: selenium webdriver, specified by pytest flags
    """
    # Generate random first name, last name, and password
    first_name = random_letter_generator()
    last_name = random_letter_generator()
    pword = random_letter_generator() + "123"

    # some basic email entries and expected status of the REGISTER button
    # False means the REGISTER button should not be clickable, opposite for True
    email_cases = {
        first_name: False,
        first_name + "@": False,
        first_name + "@gmail.co": True,
        first_name + "@gmail.com.": False
    }

    # list of top email domains that are valid, so REGISTER button should be active for these emails
    possible_email_domains = (
        # Defaults
        "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
        "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
        "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
        # Global
        "email.com", "fastmail.fm", "games.com", "gmx.net", "hush.com", "hushmail.com", "icloud.com",
        "iname.com", "inbox.com", "lavabit.com", "love.com", "outlook.com", "pobox.com", "protonmail.com",
        "rocketmail.com", "safe-mail.net", "wow.com", "ygm.com", "ymail.com", "zoho.com", "yandex.com",
        # USA
        "bellsouth.net", "charter.net", "cox.net", "earthlink.net", "juno.com",
        # British
        "btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk",
        "ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk",
        "virgin.net", "wanadoo.co.uk", "bt.com",
        # Asian
        "sina.com", "sina.cn", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp",
        "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph", "163.com", "126.com", "aliyun.com",
        "foxmail.com",
        # French
        "hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr",
        "free.fr",
        # German
        "gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de",
        # Italian
        "libero.it", "virgilio.it", "hotmail.it", "aol.it", "tiscali.it", "alice.it", "live.it", "yahoo.it", "email.it",
        "tin.it", "poste.it", "teletu.it",
        # Russian
        "mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru",
        # Belgian
        "hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be",
        # Argentinian
        "hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar",
        # Mexico
        "yahoo.com.mx", "live.com.mx", "hotmail.es", "hotmail.com.mx", "prodigy.net.mx",
        # Brazil
        "yahoo.com.br", "hotmail.com.br", "outlook.com.br", "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br",
        "itelefonica.com.br", "r7.com", "zipmail.com.br", "globo.com", "globomail.com", "oi.com.br")

    # fill in non-email fields
    fill_individual_form(selenium, first_name, last_name, "", pword, checkbox=True)

    # get the REGISTER button element, for use to determine if it is clickable
    register_button = dom.get_element(selenium, REGISTER_BTN)

    # check the status of the REGISTER button for basic email entries
    for email_text, expected_condition in email_cases.items():
        # fill in the email field
        dom.set_element_value(selenium, EMAIL, email_text)
        # get status of REGISTER button
        actual_condition = register_button.is_enabled()
        # confirm status of REGISTER button
        assert expected_condition == actual_condition, \
            "Expected 'Register' Button enabled status to be {}, but was actually {}".format(expected_condition, actual_condition)

    # confirm REGISTER button is clickable for top email domains
    for domain in possible_email_domains:
        # fill in the email field
        dom.set_element_value(selenium, EMAIL, "{}@{}".format(first_name, domain))
        # confirm status of REGISTER button is clickable
        assert register_button.is_enabled(), \
            "Expected 'Register' Button enabled status to be True, but was actually False"


def random_letter_generator(size=6):
    """
    Generates a 5 letter and 1 number string

    :param size: size of the string to be returned
    :return: str, a 5 letter and 1 number string
    """
    return ''.join(random.choice(string.ascii_lowercase) for i in range(size - 1)) + random.choice(string.digits)


def fill_individual_form(driver, firstname, lastname, email, pword, checkbox=False):
    """
    Fills in the individual registration form

    :param driver: webdriver
    :param firstname: str, first name
    :param lastname: str, last name
    :param email: str, email
    :param pword: str, password
    :param checkbox: bool, True to check the agreement checkbox
    """
    information = {
        FIRSTNAME: firstname,
        LASTNAME: lastname,
        EMAIL: email,
        PASSWORD: pword
    }

    for field, text in information.items():
        dom.set_element_value(driver, field, text)

    if checkbox:
        dom.click_element(driver, CHECKBOX, must_be_visible=False)

