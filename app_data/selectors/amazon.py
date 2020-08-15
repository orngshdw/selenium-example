"""
CSS Selectors for amazon tests
"""
""" HOME PAGE """
# ----- main search input ----- #
INPUT_SCOPE = '.nav-search-scope'
INPUT_FIELD = 'input#twotabsearchtextbox'
INPUT_SEARCH_BUTTON = 'input.nav-input'
CART_ICON = '#nav-cart'


""" RESULTS PAGE """
# ----- messages to user ----- #
# result stats that display on search results
UPPER_RESULT_INFO = '[cel_widget_id="UPPER-RESULT_INFO_BAR"] .sg-col-inner'
# disclaimer message
TOP_BANNER_MESSAGE = '[cel_widget_id="MAIN-TOP_BANNER_MESSAGE"]'

# ----- results page elements ----- #
RESULTS_CONTAINER = '.s-search-results'
AMAZON_CHOICE = '[aria-label="Amazon\'s Choice"] .a-badge-region'

# ----- buttons at bottom of page to show more results ----- #
NEXT_BUTTON = "li.a-last"


""" PRODUCT PAGE """
PRODUCT_TITLE = '#productTitle'
ADD_TO_CART_BUTTON = '#add-to-cart-button'
VIEW_CART_BUTTON = '[id*="view-cart"]'


""" VIEW CART PAGE """
CART_PRODUCT_TITLE = '.sc-product-title'
