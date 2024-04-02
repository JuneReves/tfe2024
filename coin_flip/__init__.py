from otree.api import *
import random
from math import floor, ceil
from copy import copy

doc = """
Your app description
"""

class T:
        COIN_RESULTS = {
            'Heads': 'עץ',
            'Tails': 'פלי',
            '': ''
        }
        CORRECTNESS = {
            True: 'נכון',
            False: 'לא נכון'
        }
        WONLOSS = {
            True: 'זכית',
            False: 'לא זכית'
        }

class C(BaseConstants):
    NAME_IN_URL = 'cf'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 30



class Subsession(BaseSubsession):
    coinResult = models.StringField()

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    #True for heads, False for tails
    choice = models.StringField(
        choices = [
            ['Heads', T.COIN_RESULTS['Heads']],
            ['Tails', T.COIN_RESULTS['Tails']]           
        ],
        initial='',
        widget=widgets.RadioSelectHorizontal,
    )
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0, min=0)

    def get_res_num(self, round):
        num_of_heads = []
        num_of_tails = []
        heads_per = []
        tails_per = []
        flip_result = []
        player_choices = []
        for i in range(round):
            player = self.in_round(i+1)
            if player.choice == 'Heads':
                player_choices.append('Heads')
            elif player.choice == 'Tails':
                player_choices.append('Tails')
            else:
                player_choices.append('')
            num_of_heads.append(0)  
            num_of_tails.append(0)
            flip_result.append(self.subsession.in_round(i+1).coinResult)
            for p in self.subsession.get_players():
                if p.in_round(i+1).choice == 'Heads':
                    num_of_heads[-1] += 1
                elif p.in_round(i+1).choice == 'Tails':
                    num_of_tails[-1] += 1
            players_list = self.subsession.get_players()
            numOfPartThatAnswered = len(list(filter(lambda x: x.in_round(i+1).choice != '', players_list)))
            try:
                heads_per.append(floor(num_of_heads[-1]*100/numOfPartThatAnswered))
            except ZeroDivisionError:
                heads_per.append(0)
            try:
                tails_per.append(floor(num_of_tails[-1]*100/numOfPartThatAnswered))
            except ZeroDivisionError:
                tails_per.append(0)
        return num_of_heads, num_of_tails, heads_per, tails_per, player_choices, flip_result
    

    def count_wins(self):
        counter = 0
        for p in self.in_all_rounds():
            if p.payoff > 0:
                counter += 1
        return counter
    



class FlipPage(Page):

    timeout_seconds = 30
    form_model = 'player'
    form_fields = ['choice']
    def vars_for_template(player):
        players_num = player.session.num_participants
        heads, tails, heads_per, tails_per, player_choices, flip_results = player.get_res_num(round=player.round_number-1)
        data = [
            {'round': i+1, 'heads': heads[i],
            'heads_per': heads_per[i], 'tails': tails[i],
            'tails_per': tails_per[i], 'correctness': T.CORRECTNESS[player_choices[i]==flip_results[i]],
            'result': T.COIN_RESULTS[flip_results[i]], 'rank': player.in_round(i+1).rank,
            'total': tails[i]+heads[i], 'percentile': floor(100*player.in_round(i+1).rank/players_num),
            'payoff': int(player.in_round(i+1).payoff)}
             for i in range(player.round_number-1)]
        data.reverse()
        return dict(
            num = floor(player.session.config['condition']*players_num),
            gain = int(player.session.config['round_bonus']),
            percent = int(player.session.config['condition']*100),
            data = data,
            timer_text = 'זמן שנותר לבחירה:'
        )
    



class FlipResult(Page):

    timeout_seconds = 30
    def vars_for_template(player):
        players_num = player.session.num_participants
        heads, tails, heads_per, tails_per, player_choices, flip_results = player.get_res_num(round=player.round_number)
        data = [
            {'round': i+1, 'heads': heads[i],
            'heads_per': heads_per[i], 'tails': tails[i],
            'tails_per': tails_per[i], 'correctness': T.CORRECTNESS[player_choices[i]==flip_results[i]],
            'result': T.COIN_RESULTS[flip_results[i]], 'rank': player.in_round(i+1).rank,
            'total': players_num, 'percentile': floor(100*player.in_round(i+1).rank/players_num),
            'payoff': int(player.in_round(i+1).payoff)}
             for i in range(player.round_number)]
        data.reverse()
        return dict(
            coin_result = T.COIN_RESULTS[player.subsession.coinResult],
            guess = T.COIN_RESULTS[player.choice],
            rank = player.rank,
            total = players_num,
            status = T.WONLOSS[player.payoff>0],
            payoff = player.session.config['round_bonus'],
            num = floor(player.session.config['condition']*players_num),
            gain = int(player.session.config['round_bonus']),
            percent = int(player.session.config['condition']*100),
            data = data,
            timer_text = 'הניסוי ימשיך באופן אוטומטי בעוד:'
        )
    

class Results(Page):
    
    def is_displayed(player):
        round_cut = min(C.NUM_ROUNDS, player.session.config['round_cut'])
        return player.round_number == round_cut
    
    def app_after_this_page(player, upcoming_apps):
        return 'survey'

    def vars_for_template(player):
        players_num = player.session.num_participants
        percent_of_players = floor(player.session.config['condition']*players_num)
        heads, tails, heads_per, tails_per, player_choices, flip_results = player.get_res_num(round=player.round_number)
        data = [
            {'round': i+1, 'heads': heads[i],
            'heads_per': heads_per[i], 'tails': tails[i],
            'tails_per': tails_per[i], 'correctness': T.CORRECTNESS[player_choices[i]==flip_results[i]],
            'result': T.COIN_RESULTS[flip_results[i]], 'rank': player.in_round(i+1).rank,
            'total': players_num, 'percentile': floor(100*player.in_round(i+1).rank/players_num),
            'payoff': int(player.in_round(i+1).payoff)}
             for i in range(player.round_number)]
        data.reverse()
        return dict(
            rank = player.rank,
            players_num = players_num,
            wins = player.count_wins(),
            points = int(player.participant.payoff),
            payoff = player.participant.payoff_plus_participation_fee(),
            data = data,
        )

class afterRoundPage(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.coinResult = 'Heads' if random.randint(0, 2) == 1 else 'Tails'
        for p in subsession.get_players():
            if subsession.round_number > 1:
                new_score = copy(p.in_round(subsession.round_number -1).score)
            else:
                new_score = 0
            if p.choice == subsession.coinResult:
                new_score += 1
            p.score = new_score
        sorted_players = sorted(subsession.get_players(), reverse=True,
                                key=lambda p: p.score)
        winning_cut = max(floor(subsession.session.config['condition']*len(sorted_players)),1)
        winning_score = copy(sorted_players[winning_cut-1].score)
        r = 0
        d = 1
        cur = -1 #current lowest score
        for p in sorted_players: #for every player
            if p.score >= winning_score: #If their score is higher than the winning score
                p.payoff = subsession.session.config['round_bonus'] #Give Bonus
            if p.score == cur: #If the rank is equal to that of the previous player
                d += 1 #Remember to add one more to the one with the lower score
            else: #otherwise (It is lower)
                r += d #Add difference
                d = 1 #reset difference
                cur = copy(p.score) #Current lowese
            p.rank = r #Set current player's rank

    title_text = 'אנא המתן'
    body_text = 'יש להמתין שכל השחקנים יסיימו את התור. מיד לאחר מכן תמשיך הלאה באופן אוטומטי.'

class waitPage(WaitPage):
    wait_for_all_groups = True
    title_text = 'אנא המתן'
    body_text = 'יש להמתין שכל השחקנים יסיימו את התור. מיד לאחר מכן תמשיך הלאה באופן אוטומטי.'


class waitToStart(WaitPage):
    wait_for_all_groups = True
    def is_displayed(player):
        return player.round_number == 1
    title_text = 'מיד מתחילים'
    body_text = 'הניסוי יתחיל מיד לאחר שכל השחקנים יהיו מוכנים.'

class InstructionPage(Page):
    def is_displayed(player):
        return player.round_number == 1
    def vars_for_template(player):
        num_of_players = floor(player.session.config['condition']*player.session.num_participants)
        return dict(
            num = num_of_players,
            gain = int(player.session.config['round_bonus']),
            percent = int(player.session.config['condition']*100)
        )
    

page_sequence = [InstructionPage, waitToStart, FlipPage, afterRoundPage, FlipResult, Results, waitPage]
