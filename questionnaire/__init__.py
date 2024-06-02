from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'qn'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField(min_length=7, max_length=15)

# PAGES
class questionnaire(Page):
    form_model = 'player'
    form_fields=[
        'prolific_id'
    ]

class intro(Page):
        pass


page_sequence = [intro, questionnaire]
