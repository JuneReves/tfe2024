from os import environ

SESSION_CONFIGS = [
    dict(
        name='Main',
        app_sequence=['questionnaire','coin_flip', 'last_page'],
        num_demo_participants=5,
        condition=[0.2,0.8],
        round_bonus=[50,10],
        round_cut=30
    ),
    dict(
        name='Test',
        app_sequence=['coin_flip', 'last_page'],
        num_demo_participants=5,
        condition=[0.2,0.8],
        round_bonus=[50,10],
        round_cut=5
    ),

]

ROOMS = [
        dict(
        name='test',
        display_name='Test Room'
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.334, participation_fee=0.00, doc="", condition=[0.2,0.8], round_bonus=[50,10], round_cut=30
)

PARTICIPANT_FIELDS = ['treatment_group', 'dropout']
SESSION_FIELDS = ['first_player_arrived', 'redefined_groups']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = '₪'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2036959895086'
