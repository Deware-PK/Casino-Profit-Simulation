import random
from enum import Enum
from module.casino import Player, Bet_Category
import logging
from datetime import datetime
import argparse
import configparser

config = configparser.ConfigParser() # Creating a configParser object
config.read("settings.ini")    # Reading the config file
dice_config = config.sections()

# Create a custom formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%m-%d-%Y %I:%M %p')

# Create a file handler with the current date and time in the file name
log_filename = datetime.now().strftime('%m-%d-%Y_%I-%M-%S_%p.log')
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Add the file handler to the root logger
logging.root.addHandler(file_handler)

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class GameResult(Enum):
    NONE = 0
    LOW = 1
    HIGH = 2

# Roll 2 dices and return their sum.
def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

# Categorize the summary of two dice
def categorize_sum(dice_sum):
    if 2 <= dice_sum <= 6:
        return GameResult.LOW
    elif 7 <= dice_sum <= 12:
        return GameResult.HIGH
    else:
        return GameResult.NONE # no return for incorrect bets

def calculate_payout_rate(player, dice_sum):
    house_edge_multipliers = {
        2: int(config[dice_config[1]]['number_2']),
        3: int(config[dice_config[1]]['number_3']),
        4: int(config[dice_config[1]]['number_4']),
        5: int(config[dice_config[1]]['number_5']),
        6: int(config[dice_config[1]]['number_6']),
        7: int(config[dice_config[1]]['number_7']),
        8: int(config[dice_config[1]]['number_8']),
        9: int(config[dice_config[1]]['number_9']),
        10: int(config[dice_config[1]]['number_10']),
        11: int(config[dice_config[1]]['number_11']),
        12: int(config[dice_config[1]]['number_12'])
    }

    bet_choice = player.get_bet_choice()
    sum_category = categorize_sum(dice_sum)

    if bet_choice == Bet_Category.LOW.value:
        return 2 if sum_category == GameResult.LOW else 0
    elif bet_choice == Bet_Category.HIGH.value:
        return 1.95 if sum_category == GameResult.HIGH else 0
    elif bet_choice == Bet_Category.SINGLE.value:
        single_bet_choice = player.get_single_bet_choice()
        return house_edge_multipliers[single_bet_choice] if dice_sum == single_bet_choice else 0
    else:
        return 0


def game_simulation(num_players, times):
    players = [Player(i) for i in range(1, num_players + 1)]
    initial_wallets = {player.id: player.get_wallet() for player in players}
    total_stake = 0
    total_payout = 0

    for round_num in range(1, times + 1):
        dice_sum = roll_dice()
        logger.info('')
        logger.info(f"Round {round_num}")
        logger.info(f"Dice result: {dice_sum} {'HIGH' if categorize_sum(dice_sum) == GameResult.HIGH else 'LOW'}")
        
        for player in players:

            if (player.get_wallet() <= 0):
                continue

            player.set_bet_choice(random.randint(1, 3))

            if player.get_bet_choice() == Bet_Category.SINGLE.value:
                player.set_single_bet_choice(random.randint(2, 12))

            stake = random.randint(1, int(player.get_wallet()))
            player.set_stake(stake)
            total_stake += stake

            logger.info(f"[Player {player.id}] Betting on {'LOW' if player.get_bet_choice() == Bet_Category.LOW.value else 'HIGH' if player.get_bet_choice() == Bet_Category.HIGH.value else f'Single {player.get_single_bet_choice()}'} || Stake: {player.get_stake()} || Wallet: {player.get_wallet()}")
            
            multiplier = calculate_payout_rate(player, dice_sum)
            payout = player.get_stake() * multiplier
            player.add_wallet(int(payout))
            total_payout += int(payout)

        logging.info('')

    for player in players:
        profit = player.get_wallet() - initial_wallets[player.id]
        logger.info(f"[Player {player.id}] Wallet: {player.get_wallet()} || Profit: {profit}")


    house_profit = total_stake - total_payout
    logger.info('')
    logger.info(f"Summary after {times} rounds:")
    logger.info(f"Total Stake: {total_stake}")
    logger.info(f"Total Payout: {total_payout}")
    logger.info(f"House Hold Profit: {house_profit}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a dice game")
    parser.add_argument("num_players", type=int, help="Number of players")
    parser.add_argument("times", type=int, help="Number of simulation rounds")
    args = parser.parse_args()

    game_simulation(args.num_players, args.times)

