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
    gender = models.StringField(
        label='gender',
        choices=[
            ['Male', 'גבר'],
            ['Female', 'אישה'],
            ['Other', 'אחר'],
            ['Irrelevant', 'מעדיפ.ה לא לציין']
        ]
    )
    age = models.IntegerField(min=0, max=130)
    field_of_study = models.StringField(label='Field')
    degree = models.StringField(
    choices=[
        ['bachelor', 'בוגר'],
        ['Master', 'מוסמך'],
        ['PHD', 'דוקטורט'],
        ['Other', 'אחר']]
        )
    birth_country = models.StringField(label='birth country'

        )
    alyia_year = models.IntegerField(
        label='aliya', min=1948, max=2020, blank=True)
    degree_year = models.StringField(label='degree_year',
    choices=[
        ['1', 1],
        ['2', 2],
        ['3', 3],
        ['4', 4],
        ['More', '5 או יותר']
    ],
        )
    math_units = models.IntegerField(min=0, max=5, label='math_units')
    grades_average = models.FloatField(min=0, max=100, label='grades_average')
    work_status = models.StringField(
        label='work_status',
        choices=[['1', 'לא עובד/ת'], ['2', 'עובד/ת במשרה חלקית'],
            ['3', 'עובד/ת במשרה מלאה']],
        widget=widgets.RadioSelectHorizontal,

    )
    smoking = models.StringField(
        label='smoking',
        choices=[['Yes', 'כן'], ['No', 'לא']],
        widget=widgets.RadioSelectHorizontal,

    )
    past_smoking = models.StringField(
        label='past_smoking',
        choices=[['Yes', 'כן'], ['No', 'לא']],
        widget=widgets.RadioSelectHorizontal,

    )
    religious_status = models.StringField(
        label='religion_status',
        choices=[
            ['very', 'מאד דתי'],
            ['religious', 'דתי'],
            ['traditional', 'מסורתי'],
            ['secular', 'חילוני'],
            ['Not', 'לא דתי']
        ],
        widget=widgets.RadioSelectHorizontal,

    )
    Life_insurance = models.StringField(
        label='life_insurance',
        choices=[
            ['Yes', 'כן'],
            ['No', 'לא'],
            ['idk', 'לא יודע']
        ],
        widget=widgets.RadioSelectHorizontal,

    )
    pension = models.StringField(
        label='pension',
        choices=[
            ['Yes', 'כן'],
            ['No', 'לא'],
            ['idk', 'לא יודע']
        ],
        widget=widgets.RadioSelectHorizontal,

    )
    bank_freq = models.StringField(
        label='bank',
                choices=[
            ['every day', 'כל יום'],
            ['Every week', 'פעם בשבוע'],
            ['Every month', 'פעם בחודש'],
            ['Every few months', 'פעם בכמה חודשים'],
            ['never', 'אף פעם']
        ],
        widget=widgets.RadioSelectHorizontal,

    )
    overdraft_freq = models.StringField(
        label='overdraft',
                choices=[
                    ['Always', 'כל הזמן'],
                    ['Often', 'לעיתים קרובות'],
                    ['rarely', 'לעיתים רחוקות'],
                    ['never', 'אף פעם']
        ],
        widget=widgets.RadioSelectHorizontal,

    )
    age_85 = models.IntegerField(
        label='age_85', min=0, max=10)
    age_95 = models.IntegerField(
        label='age_95', min=0, max=10)
    money_in_a_year = models.IntegerField(label='money_in_a_year', min=0)
    Lottery = models.IntegerField(label='money_in_a_year', min=0)


# PAGES
class questionnaire(Page):
    form_model = 'player'
    form_fields=[
        'gender',
        'age',
        'birth_country',
        'alyia_year',
        'field_of_study',
        'degree_year',
        'degree',
        'math_units',
        'grades_average',
        'work_status',
        'smoking',
        'past_smoking',
        'religious_status',
        'Life_insurance',
        'pension',
        'bank_freq',
        'overdraft_freq',
        'age_85',
        'age_95',
        'money_in_a_year',
        'Lottery',
    ]

class waitToStart(WaitPage):
    wait_for_all_groups = True
    title_text = 'מיד מתחילים'
    body_text = 'נמשיך בניסוי מיד לאחר שכל המשתתפים יסיימו למלא את השאלון.'



page_sequence = [questionnaire, waitToStart]
