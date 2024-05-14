from enum import Enum
import configparser

config = configparser.ConfigParser() # Creating a configParser object
config.read("settings.ini")    # Reading the config file
player_config = config.sections()

class Bet_Category(Enum):
    NONE = 0
    LOW = 1
    HIGH = 2
    SINGLE = 3
    
class Player:
    def __init__(self, id):
        self.id = id
        self.wallet = int(config[player_config[0]]['start_up_balance'])
        self.bet_choice = None
        self.single_bet_choice = None
        self.stake = 0
        self.payout = 0

    def set_single_bet_choice(self, single_bet_choice):
        self.single_bet_choice = single_bet_choice

    def get_single_bet_choice(self):
        return self.single_bet_choice

    def set_bet_choice(self, bet_choice):
        self.bet_choice = bet_choice

    def get_bet_choice(self):
        return self.bet_choice

    def get_payout(self):
        return self.payout
    
    def set_stake(self, value):
        if value <= self.wallet:
            self.wallet -= value
            self.stake = value

    def get_stake(self):
        return self.stake
    
    def get_wallet(self):
        return self.wallet
    
    def add_wallet(self, value):
        self.wallet += value
