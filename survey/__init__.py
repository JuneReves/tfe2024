from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'final_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    exp_goal = models.LongStringField(
        label='מה לדעתך מטרת המחקר?',
        max_length=300,
    )
    instructions = models.LongStringField(
        label='האם ההוראות היו ברורות?',
        max_length=300,
    )
    felt_in_game = models.LongStringField(
        label='איך הרגשת במהלך הניסוי?',
        max_length=300,
    )
    repeat_inst = models.LongStringField(
        label='חשוב לנו לדעת האם הוראות הניסוי היו ברורות למשתתפים. לשם כך, אנא תאר/י במילים שלך את מהלך המשחק.',
        max_length=500,
    )
    comments = models.LongStringField(
        label= 'אם יש לך הערות כלשהן לגבי הניסוי, אנא רשום/רשמי אותן כאן',
        max_length=500,
    )
    


# PAGES
class survey(Page):
    form_model = 'player'
    form_fields = [
        'exp_goal',
        'instructions',
        'felt_in_game',
        'repeat_inst',
        'comments']


page_sequence = [survey]
