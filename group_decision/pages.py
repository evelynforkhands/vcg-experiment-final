
from otree.api import Page

from .VCG.VCG_pages import *
from .BordaCount.BordaCount_pages import *
from .TTC.TTC_pages import *
from .helpers import PageWithTimeout, is_correct_treatment, get_strings
from .models import Player, C


class VCG(Page):
    def is_displayed(self):
        return is_correct_treatment(self, 'VCG')

class BordaCount1(Page):
    def is_displayed(self):
        return is_correct_treatment(self, 'BordaCount')

class BordaCount2(Page):
    def is_displayed(self):
        return is_correct_treatment(self, 'BordaCount')

class TTC(Page):
    def is_displayed(self):
        return is_correct_treatment(self, 'TTC')

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):
        return {
            'strings': C.strings,
        }

    def before_next_page(self):
        import time
        if is_correct_treatment(self.player, 'BordaCount'):
            self.player.start_time_Borda = int(time.time())
        elif is_correct_treatment(self.player, 'TTC'):
            self.player.start_time_TTC = int(time.time())
        elif is_correct_treatment(self.player, 'VCG'):
            self.player.start_time_VCG = int(time.time())
        else:
            return 0
        

class TaskIntro(Page):

    def vars_for_template(self):
        return {
            'order': self.group.round_number,
            'strings': C.strings
        }
    
    def before_next_page(self):
        import time
        if is_correct_treatment(self.player, 'BordaCount'):
            self.player.start_time_Borda = int(time.time())
        elif is_correct_treatment(self.player, 'TTC'):
            self.player.start_time_TTC = int(time.time())
        elif is_correct_treatment(self.player, 'VCG'):
            self.player.start_time_VCG = int(time.time())
        else:
            return 0
        
class TaskOutro(PageWithTimeout):

    def vars_for_template(self):
        return {
            'order': self.group.round_number,
            'strings': C.strings
        }
    
    def before_next_page(self):
        print('before_next_page')
        print(self.player.round_number)
        print(self.player.round_number)
        if self.player.round_number == C.NUM_ROUNDS:
            self.player.group.set_payoffs_1()
        

class Satisfaction(PageWithTimeout):
    form_model = 'player'
    form_fields = ['satisfaction', 'dissatisfaction', 'understanding', 'appropriateness', 'fairness']

    def vars_for_template(self):
        current_round = self.player.round_number
        current_treatment = getattr(self.player.participant, f'treatment_round_{current_round}')
        return {
            'current_treatment': current_treatment,
            'round_number': current_round,
            'strings': C.strings, 
            'assigned_room': self.player.assigned_room,
            'assigned_room_rank': self.player.assigned_room_rank if current_treatment in ['BordaCount', 'TTC'] else None,
            'bids': self.player.get_sorted_bids() if current_treatment == 'VCG' else None,
            'pivotal': self.player.pivotal if current_treatment == 'VCG' else None,
            'payment': self.player.payment_vcg if current_treatment == 'VCG' else None, 
        }
    

class Trust(PageWithTimeout):
    form_model = 'player'
    form_fields = ['benevolence', 'competence', 'integrity']
    

    def vars_for_template(self):
        current_round = self.player.round_number
        current_treatment = getattr(self.player.participant, f'treatment_round_{current_round}')
        return {
            'order': self.group.round_number,
            'strings': C.strings,
            'treatment': current_treatment
        }
    
class Payoff(Page):
    form_model = 'player'

    def vars_for_template(self):
        print()
        return {
            'payoff': self.participant.payoff,
            'payoff_part': int(self.player.payoff_points) * C.POINTS_TO_EUR,
            'part_to_pay': self.player.part_to_pay,
            'payoff_points': int(self.player.payoff_points),
            'total_payoff': self.participant.payoff_plus_participation_fee(),

        }

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS



page_sequence = [Introduction, TaskIntro, InfoVCG, TestVCG_1, TestVCG_2, DecisionVCG, WaitForVCG, OutcomeVCG,InfoBordaCount, TestBordaCount_1, TestBordaCount_2, DecisionBordaCount,WaitForBordaCount, OutcomeBordaCount, InfoTTC, TestTTC_1, TestTTC_2, DecisionTTC, WaitForTTC, OutComeTTC, TaskOutro, Satisfaction, Trust, Payoff]