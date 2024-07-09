from otree.api import *
from random import randint
from math import floor
from copy import copy
from time import time

doc = """
Your app description
"""

class T:
        CORRECTNESS = {
            True: 'correct',
            False: 'incorrect'
        }
        WONLOSS = {
            True: 'did',
            False: 'did not'
        }
        WAIT_FOR_ALL = 'Please wait for all participants to arrive'
        WAIT_TO_START = 'The game will begin once all participants have announced that they are ready.'
        PW = 'Please wait'


class C(BaseConstants):
    NAME_IN_URL = 'cf'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 30
    # TREATMENTS = [1,2]

def creating_session(subsession):
    if subsession.round_number == 1:
        subsession.session.first_player_arrived = 0
        subsession.session.redefined_groups = False
        t = subsession.session.config['treatment_group']
        for i, player in enumerate(subsession.get_players()):
            player.participant.treatment_group = t

    subsession.flip_coin()

def set_start_time(subsession):
    if subsession.session.first_player_arrived == 0:
        subsession.session.first_player_arrived = time()



class Subsession(BaseSubsession):
    coinResult = models.StringField()
    numOfHeads_c1 = models.IntegerField(default=0)
    numOfTails_c1 = models.IntegerField(default=0)
    numOfHeads_c2 = models.IntegerField(default=0)
    numOfTails_c2 = models.IntegerField(default=0)

    def coin_sides(subsession, text): # To quickly compensate for the change of heads and tales
        if text.lower() == 'heads':
            return subsession.session.config['heads_name']
        if text.lower() == 'tails':
            return subsession.session.config['tails_name']
        return ''


    def get_players_by_treatment(subsession, treatment):
        players = subsession.get_players()
        new_players = filter(lambda p: p.participant.treatment_group == treatment, players)
        return list(new_players)
    

    def flip_coin(subsession):
        subsession.coinResult = 'Heads' if randint(0, 1) == 1 else 'Tails'
    

    #count responses
    def count_responses_for_group(subsession, treatment):
        heads = 0
        tails = 0
        players = subsession.get_players_by_treatment(treatment)
        for p in players:
            if p.choice == 'Heads':
                heads+=1
            elif p.choice == 'Tails':
                tails+=1
        return heads, tails


    def count_and_set_responses(subsession):
        subsession.numOfHeads_c1, subsession.numOfTails_c1 = subsession.count_responses_for_group(1)
        subsession.numOfHeads_c2, subsession.numOfTails_c2 = subsession.count_responses_for_group(2)


    def sort_and_reward(subsession, treatment):
        sorted_players = sorted(subsession.get_players_by_treatment(treatment), reverse=True,
                                key=lambda p: p.score)
        winning_cut = max(floor(subsession.session.config['condition'][treatment-1]*len(sorted_players)),1)
        winning_score = copy(sorted_players[winning_cut-1].score)
    
        r = 0
        d = 1
        cur = -1 #current lowest score
        for p in sorted_players: #for every player
            p.payoff = 0
            if p.score >= winning_score: #If their score is higher than the winning score
                if p.choice == subsession.coinResult: #And they guessed right
                    p.payoff = p.get_bonus() #Give Bonus
                    p.cumulativePayoff += p.get_bonus()
            if p.score == cur: #If the rank is equal to that of the previous player
                d += 1 #Remember to add one more to player one with the lower score
            else: #otherwise (It is lower)
                r += d #Add difference
                d = 1 #reset difference
                cur = copy(p.score) #Current lowest
            p.rank = r #Set current player's rank


    def set_scores(subsession):
        for p in subsession.get_players():
            if subsession.round_number > 1:
                new_score = copy(p.in_round(subsession.round_number -1).score)
            else:
                new_score = 0
            if p.choice == subsession.coinResult:
                new_score += 1
            p.score = new_score
            p.cumulativePayoff = p.participant.payoff




class Group(BaseGroup):
    pass


class Player(BasePlayer):

    #True for heads, False for tails
    choice = models.StringField(
        initial='',
        choices=['Heads', 'Tails']
        # widget=widgets.RadioSelectHorizontal,
    )
    def choice_choices(player):
        return [['Heads', player.session.config['heads_name']], ['Tails', player.session.config['heads_name']]]           

    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0, min=0)
    cumulativePayoff = models.CurrencyField(default=0)

    def get_same_treatment_players(self):
        return self.subsession.get_players_by_treatment(self.participant.treatment_group)
    

    def get_treatment_results(self):
        if self.participant.treatment_group == 1:
            return self.subsession.numOfHeads_c1, self.subsession.numOfTails_c1
        return self.subsession.numOfHeads_c2, self.subsession.numOfTails_c2



    def get_res_num(self, round):
        heads = []
        tails = []
        heads_per = []
        tails_per = []
        flip_result = []
        c_payoff = []
        correct_guesses = []

        for i in range(round):
            player = self.in_round(i+1)
            num_of_heads, num_of_tails = self.in_round(i+1).get_treatment_results()
            heads.append(num_of_heads)
            tails.append(num_of_tails)
            flip_result.append(self.subsession.in_round(i+1).coinResult)
            correct_guesses.append(flip_result[-1]==player.choice)
            numOfPartThatAnswered = num_of_heads + num_of_tails
            if numOfPartThatAnswered != 0:
                heads_per.append(floor(num_of_heads*100/numOfPartThatAnswered))
                tails_per.append(floor(num_of_tails*100/numOfPartThatAnswered))
            else:
                heads_per.append(0)
                tails_per.append(0)
            c_payoff.append(player.cumulativePayoff)
        return heads, tails, heads_per, tails_per, flip_result, c_payoff, correct_guesses
    

    def get_table_data(player, players_num, round_diff=0):
        heads, tails, heads_per, tails_per, flip_results, c_payoff, correct_guesses = player.get_res_num(round=player.round_number+round_diff)
        return [
            {'round': i+1,
            'heads': heads[i],
            'heads_per': heads_per[i],
            'tails': tails[i],
            'tails_per': tails_per[i],
            'correctness': T.CORRECTNESS[correct_guesses[i]],
            'result': player.subsession.coin_sides(flip_results[i]),
            'rank': player.in_round(i+1).rank,
            'total': players_num,
            'percentile': floor(100*player.in_round(i+1).rank/players_num),
            'payoff': int(player.in_round(i+1).payoff),
            'c_payoff': int(c_payoff[i])}
            for i in range(player.round_number+round_diff)]

    def count_wins(self):
        counter = 0
        for p in self.in_all_rounds():
            if p.payoff > 0:
                counter += 1
        return counter
    
    def get_bonus(self):
        return self.session.config['round_bonus'][self.participant.treatment_group-1]
    
    def get_cond(self):
        return self.session.config['condition'][self.participant.treatment_group-1]



class FlipPage(Page):

    timeout_seconds = 30
    form_model = 'player'
    form_fields = ['choice']
    def vars_for_template(player):
        players_num = len(player.get_same_treatment_players())
        data = player.get_table_data(players_num, -1)
        split_table = len(data) > 15
        if split_table:
            data1 = data[:15]
            data2 = data[15:]
        else:
            data1 = data[:]
            data2 = []
        data.reverse()
        return dict(
            num = floor(player.get_cond()*players_num),
            gain = int(player.get_bonus()),
            percent = int(player.get_cond()*100),
            data1 = data1,
            data2 = data2,
            data = data,
            split = split_table,
            heads = player.subsession.session.config['heads_name'],
            tails = player.subsession.session.config['tails_name'],
        )
    



class FlipResult(Page):
    timeout_seconds = 30
    def vars_for_template(player):
        players_num = len(player.get_same_treatment_players())
        data = player.get_table_data(players_num)
        split_table = len(data) > 15
        if split_table:
            data1 = data[:15]
            data2 = data[15:]
        else:
            data1 = data[:]
            data2 = []
        data.reverse()
        return dict(
            coin_result = player.subsession.coin_sides(player.subsession.coinResult),
            guess = player.subsession.coin_sides(player.choice),
            rank = player.rank,
            total = players_num,
            status = T.WONLOSS[player.payoff>0],
            payoff = player.session.config['round_bonus'],
            num = floor(player.get_cond()*players_num),
            gain = int(player.get_bonus()),
            percent = int(player.get_cond()*100),
            data1 = data1,
            data2 = data2,
            data = data,
            split = split_table,
            heads = player.subsession.session.config['heads_name'],
            tails = player.subsession.session.config['tails_name'],
        )
    

class Results(Page):
    
    def is_displayed(player):
        round_cut = min(C.NUM_ROUNDS, player.session.config['round_cut'])
        return player.round_number == round_cut
    
    def app_after_this_page(player, upcoming_apps):
        return 'last_page'

    def vars_for_template(player):
        players_num = len(player.get_same_treatment_players())
        data = player.get_table_data(players_num)
        data.reverse()
        return dict(
            rank = player.rank,
            players_num = players_num,
            wins = player.count_wins(),
            gain = int(player.get_bonus()),
            points = int(player.participant.payoff),
            payoff = player.participant.payoff_plus_participation_fee(),
            data = data,
            heads = player.subsession.session.config['heads_name'],
            tails = player.subsession.session.config['tails_name'],
        )

class afterRoundPage(WaitPage):
    wait_for_all_groups = True
    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.count_and_set_responses()
        
        subsession.set_scores()
        
        subsession.sort_and_reward(subsession.session.config['treatment_group'])


    title_text = T.PW
    body_text = T.WAIT_FOR_ALL

class waitPage(WaitPage):
    title_text = T.PW
    body_text = T.WAIT_FOR_ALL



class waitToStart(WaitPage):
    wait_for_all_groups = True
    title_text = T.PW
    body_text = T.WAIT_TO_START


class InstructionPage(Page):
    def is_displayed(player):
        if player.round_number == 1:
            return True
        return False
    def vars_for_template(player):
        num_of_players = floor(player.get_cond()*len(player.get_same_treatment_players()))
        return dict(
            num = num_of_players,
            gain = int(player.get_bonus()),
            percent = int(player.get_cond()*100),
            heads = player.subsession.session.config['heads_name'],
            tails = player.subsession.session.config['tails_name'],
        )
    

page_sequence = [InstructionPage, waitToStart, FlipPage, afterRoundPage, FlipResult, Results, waitPage]
