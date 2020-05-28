"""
pytest/pytest-selenium configuration file.

Defines pytest flags that allow setting up of test conditions before executing tests;
such as running tests in a headless browser or at a specified window resolution.
"""
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()))

DEFAULT_RESOLUTION = "1024, 768"


def pytest_addoption(parser):
    """
    Defines pytest flags

    :param parser: parser for commandline arguments
    """
    parser.addoption(
        "--headless",
        action="store_true",
        help="Specifies to run test in headless mode."
    )


@pytest.fixture
def chrome_options(chrome_options, is_headless):
    """
    Handles Chrome configuration options

    :param pytestconfig: pytest-selenium ficture
    :param is_headless: fixture defined (below)
    :return: bool
    """
    # sets headless configuration
    if is_headless:
        chrome_options.add_argument('headless')
    # sets browser resolution
    chrome_options.add_argument("--window-size={}".format(DEFAULT_RESOLUTION))
    return chrome_options


@pytest.fixture(scope='session')
def is_headless(pytestconfig):
    """
    Handles running tests in headless browser

    :param pytestconfig: pytest configuration options
    :param request: pytest fixture
    :return: bool
    """
    # Set defaults when --headless is specified
    if pytestconfig.getoption('--headless'):
        return True
    return False

