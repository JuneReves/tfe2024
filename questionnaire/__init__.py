from otree.api import *
from coin_flip import C, set_start_time, T
from time import time


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
    prolific_id = models.StringField(min_length=2, max_length=50)

# PAGES
class questionnaire(Page):

    timer_text = T.START_TIMER_TEXT

    form_model = 'player'
    form_fields=[
        'prolific_id'
    ]
    def get_timeout_seconds(player):
        timer = C.WAIT_FOR_PARTICIPANTS - (time() - player.session.first_player_arrived)
        if timer <= 0:
            player.participant.vars['dropout'] = True
            return 0
        else:
            return timer


class intro(Page):

    timer_text = T.START_TIMER_TEXT

    def is_displayed(player):
        set_start_time(player.subsession)
        return True
    
    def get_timeout_seconds(player):
        timer = C.WAIT_FOR_PARTICIPANTS - (time() - player.session.first_player_arrived)
        if timer <= 0:
            player.participant.vars['dropout'] = True
            return 0
        else:
            return timer
        
        




page_sequence = [intro, questionnaire]
