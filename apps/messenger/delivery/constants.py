# ~ MODELS
# ----------------------------------
PACK_MODEL = "Pack"
PRODUCT_MODEL = "Product"
SHIPPING_ADDRESS_MODEL = "Adress"
LOCATION_MODEL = "Location"
ORDER_MODEL = "Order"

# ~ STATES
# ----------------------------------
START = "start"
INFO = "info"
LOGIN = "login"


ORDER_MENU = "order_menu"
NEW_ORDER = "new_order"
ORDER_LIST = "order_list"
ORDERS_TRACKING = "orders_tracking"


PROCESS_CODE = "process_code"
PRODUCT_MENU = "product_menu"
SEARCH_ITEM = "search_item"
PACK_LIST = "pack_list"


ADDRESS_MENU = "address_menu"
ADDRESS_LIST = "address_list"
ORDER_DETAIL = "order_detail"
SUCCESS_MESSAGE = "success_message"

PHRASE = "phrase"

CURRENT_ORDER = "current_order"


GAME_INFO = "game_info"
SHOW_HELP_GAME = "show_help_game"

PROCESS_PLAYERS = "process_players"
CHALLENGE = "challenge"
CHALLENGE_FAST = "challenge_fast"

PLAYERS_LIST = "players_list"

SHOW_RANKING_SUCKS = "show_ranking_sucks"

JOKE = "joke"

# ~ TRIGGERS
# ----------------------------------
SHOW_START = "show_start"
SHOW_INFO = "show_info"
SHOW_LOGIN = "show_login"

SHOW_ORDER_MENU = "show_order_menu"
SHOW_NEW_ORDER = "show_new_order"
SHOW_ORDER_LIST = "show_order_list"
SHOW_ORDERS_TRACKING = "show_orders_tracking"

SHOW_PROCESS_CODE = "show_process_code"
SHOW_PRODUCT_MENU = "show_product_menu"
SHOW_UNITS = "show_units"
SHOW_PACKS = "show_packs"

ADD = "add"
SHOW_ADDRESS_MENU = "show_address_menu"
SHOW_GET_LOCATION = "show_get_location"
SHOW_ADDRESS_LIST = "show_address_list"

LOCATION = "location"
ADDRESS = "address"
CONFIRM = "confirm"
CANCEL = "cancel"

SHOW_PROFILE = "show_profile"

SHOW_CURRENT_ORDER = "show_current_order"

SHOW_JOKE = "show_joke"
NEW_JOKE = "add_joke"

SHOW_GAME = "show_game"
START_GAME = "start_game"
END_GAME = "end_game"
HELP_GAME = "help_game"

RANKING_SUCKS = "ranking_sucks"

ADD_PLAYER = "add_player"

NEW_CHALLENGE = "new_challenge"
NEW_CHALLENGE_FAST = "new_challenge_fast"
START_CHALLENGES = "start_challenges"
QUICKPLAY = "quickplay"
CANCEL_CHALLENGE = "cancel_challenge"
CANCEL_CHALLENGE_FAST = "cancel_challenge_fast"

# ~ CONDITIONS
# ----------------------------------
HAS_SESSION = "has_session"
HAS_VALID_PHONE = "has_valid_phone"
HAS_VALID_PIN = "has_valid_pin"
HAS_CART = "has_cart"
HAS_PLAYERS = "has_players"


# ~ STATES CONFIG
# ----------------------------------

states = [
    START, INFO, LOGIN, JOKE,
    GAME_INFO, SHOW_HELP_GAME, SHOW_RANKING_SUCKS, PROCESS_PLAYERS, CHALLENGE, CHALLENGE_FAST, PLAYERS_LIST,
    ORDER_MENU, NEW_ORDER, ORDER_LIST, ORDERS_TRACKING,
    PROCESS_CODE, PRODUCT_MENU, SEARCH_ITEM, PACK_LIST,
    ADDRESS_MENU, ADDRESS_LIST, ORDER_DETAIL, SUCCESS_MESSAGE
]

# ~ TRANSITIONS
# ----------------------------------


transitions = [
    {
        'source': START, 'dest': INFO,
        'trigger': SHOW_INFO,
        'after': 'render_' + INFO,  # Reply
        'conditions': []
    },
    {
        'source': START, 'dest': ORDER_MENU,
        'trigger': SHOW_ORDER_MENU,
        'after': 'render_' + ORDER_MENU,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': START, 'dest': LOGIN,
        'trigger': SHOW_LOGIN,
        'after': 'render_' + LOGIN,  # Reply
        'conditions': []
    },
    { # --------------------------------------------
        'source': ORDER_MENU, 'dest': NEW_ORDER,
        'trigger': SHOW_NEW_ORDER,
        'after': 'render_' + NEW_ORDER, # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': ORDER_MENU, 'dest': ORDER_LIST,
        'trigger': SHOW_ORDER_LIST,
        'after': 'render_' + ORDER_LIST, # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': ORDER_MENU, 'dest': ORDERS_TRACKING,
        'trigger': SHOW_ORDERS_TRACKING,
        'after': 'render_' + ORDERS_TRACKING, # Reply
        'conditions': [HAS_SESSION]
    },
    { # --------------------------------------------
        'source': NEW_ORDER, 'dest': PROCESS_CODE,
        'trigger': SHOW_PROCESS_CODE,
        'after': 'render_' + PROCESS_CODE, # Reply
        'conditions': [HAS_SESSION, HAS_VALID_PHONE]
    },
    {
        'source': PROCESS_CODE, 'dest': PRODUCT_MENU,
        'trigger': SHOW_PRODUCT_MENU,
        'after': 'render_' + PRODUCT_MENU,  # Reply
        'conditions': [HAS_SESSION, HAS_VALID_PIN]
    },
    {
        'source': PRODUCT_MENU, 'dest': PACK_LIST,
        'trigger': SHOW_PACKS,
        'after': 'render_' + PACK_LIST,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': PRODUCT_MENU, 'dest': SEARCH_ITEM,
        'trigger': SHOW_UNITS,
        'after': 'render_' + SEARCH_ITEM,  # Reply
        'conditions': [HAS_SESSION]
    },
    { # --------------------------------------------
        'source': SEARCH_ITEM, 'dest': SEARCH_ITEM,
        'trigger': ADD,
        'after': 'render_' + SEARCH_ITEM,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': PACK_LIST, 'dest': PACK_LIST,
        'trigger': ADD,
        'after': 'render_' + PACK_LIST,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': PACK_LIST, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': PACK_LIST, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': []
    },
    {
        'source': SEARCH_ITEM, 'dest': ADDRESS_MENU,
        'trigger': SHOW_ADDRESS_MENU,
        'after': 'render_' + ADDRESS_MENU,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': PACK_LIST, 'dest': ADDRESS_MENU,
        'trigger': SHOW_ADDRESS_MENU,
        'after': 'render_' + ADDRESS_MENU,  # Reply
        'conditions': [HAS_SESSION, HAS_CART]
    },
    { # --------------------------------------------
        'source': ADDRESS_MENU, 'dest': ORDER_DETAIL,
        'trigger': LOCATION,
        'after': 'render_' + ORDER_DETAIL,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': ADDRESS_MENU, 'dest': START,
        'trigger': CANCEL,
        'after': 'render_' + START,  # Reply
        'conditions': []
    },
    {
        'source': ADDRESS_MENU, 'dest': ADDRESS_LIST,
        'trigger': SHOW_ADDRESS_LIST,
        'after': 'render_' + ADDRESS_LIST,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': ADDRESS_MENU, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': []
    },
    {
        'source': ADDRESS_LIST, 'dest': ADDRESS_MENU,
        'trigger': CANCEL,
        'after': 'render_' + ADDRESS_MENU,  # Reply
        'conditions': [HAS_SESSION]
    },
    { # --------------------------------------------
        'source': ADDRESS_LIST, 'dest': ORDER_DETAIL,
        'trigger': ADDRESS,
        'after': 'render_' + ORDER_DETAIL,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': ORDER_DETAIL, 'dest': SUCCESS_MESSAGE,
        'trigger': CONFIRM,
        'after': 'render_' + SUCCESS_MESSAGE,  # Reply
        'conditions': [HAS_SESSION]
    },
    {
        'source': ORDER_DETAIL, 'dest': START,
        'trigger': CANCEL,
        'after': 'render_' + START,  # Reply
        'conditions': []
    }, 
    {  # ---------------  GAME  --------------------------
        'source': START, 'dest': GAME_INFO,
        'trigger': SHOW_GAME,
        'after': 'render_' + GAME_INFO,  # Reply
        'conditions': []
    }, 
    {
        'source': GAME_INFO, 'dest': SHOW_HELP_GAME,
        'trigger': HELP_GAME,
        'after': 'render_' + SHOW_HELP_GAME,  # Reply
        'conditions': []
    }, 
    {
        'source': GAME_INFO, 'dest': PROCESS_PLAYERS,
        'trigger': START_GAME,
        'after': 'render_' + PROCESS_PLAYERS,  # Reply
        'conditions': []
    }, 
    {
        'source': SHOW_HELP_GAME, 'dest': PROCESS_PLAYERS,
        'trigger': START_GAME,
        'after': 'render_' + PROCESS_PLAYERS,  # Reply
        'conditions': []
    }, 
    {
        'source': SHOW_HELP_GAME, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': []
    }, 
    {
        'source': GAME_INFO, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': []
    }, 
    {
        'source': PROCESS_PLAYERS, 'dest': PROCESS_PLAYERS,
        'trigger': ADD_PLAYER,
        'after': 'render_' + PROCESS_PLAYERS,  # Reply
        'conditions': [HAS_PLAYERS]
    },
    {
        'source': PROCESS_PLAYERS, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': []
    }, 
    {
        'source': PROCESS_PLAYERS, 'dest': CHALLENGE,
        'trigger': START_CHALLENGES,
        'after': 'render_' + CHALLENGE,  # Reply
        'conditions': [HAS_PLAYERS]
    }, 
    {
        'source': GAME_INFO, 'dest': CHALLENGE_FAST,
        'trigger': QUICKPLAY,
        'after': 'render_' + CHALLENGE_FAST,  # Reply
        'conditions': []
    }, 
    {
        'source': CHALLENGE, 'dest': CHALLENGE,
        'trigger': NEW_CHALLENGE,
        'after': 'render_' + CHALLENGE,  # Reply
        'conditions': [HAS_PLAYERS]
    }, 
    {
        'source': CHALLENGE_FAST, 'dest': CHALLENGE_FAST,
        'trigger': NEW_CHALLENGE_FAST,
        'after': 'render_' + CHALLENGE_FAST,  # Reply
        'conditions': []
    },
    {
        'source': CHALLENGE_FAST, 'dest': START,
        'trigger': CANCEL_CHALLENGE_FAST,
        'after': 'render_' + START,  # Reply
        'conditions': []
    }, 
    {
        'source': CHALLENGE, 'dest': SHOW_RANKING_SUCKS,
        'trigger': RANKING_SUCKS,
        'after': 'render_' + SHOW_RANKING_SUCKS,  # Reply
        'conditions': [HAS_PLAYERS]
    },
    {
        'source': SHOW_RANKING_SUCKS, 'dest': START,
        'trigger': CANCEL_CHALLENGE,
        'after': 'render_' + START,  # Reply
        'conditions': []
    },
    {
        'source': SHOW_RANKING_SUCKS, 'dest': GAME_INFO,
        'trigger': START_CHALLENGES,
        'after': 'render_' + GAME_INFO,  # Reply
        'conditions': []
    },
    {  # ---------------  JOKE  --------------------------
        'source': JOKE, 'dest': GAME_INFO,
        'trigger': SHOW_GAME,
        'after': 'render_' + GAME_INFO,  # Reply
        'conditions': []
    },
    {
        'source': START, 'dest': JOKE,
        'trigger': SHOW_JOKE,
        'after': 'render_' + JOKE,  # Reply
        'conditions': []
    },
    {
        'source': JOKE, 'dest': START,
        'trigger': START,
        'after': 'render_' + START,  # Reply
        'conditions': []
    },
    {
        'source': JOKE, 'dest': JOKE,
        'trigger': NEW_JOKE,
        'after': 'render_' + JOKE,  # Reply
        'conditions': []
    }

]
