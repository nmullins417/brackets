import math
import random
import pandas as pd
import datetime

from typing import List

# odds that a team with a [index + 1] seed is chosen to win the first round, out of 256
rd_1_prob = [255, 248, 224, 208, 160, 160, 128, 128]

# odds that the higher-seeded team wins in each subsequent round, out of 256
# 2nd round, Sweet 16, Elite 8, Final Four, Championship
rd_2_and_after_prob = [192, 176, 160, 128, 128]

matchup_list = []

def round_up_to_nearest_multiple(num: int, multiple: int) -> int:
    if (num % multiple) != 0:
        return math.ceil(num / multiple)
    return int(num / multiple)

def decide_winner_for_game(higher_seed: int, lower_seed: int, round: int) -> int:
    higher_seed_1_thru_16 = round_up_to_nearest_multiple(higher_seed, 4)
    higher_seed_win_prob = rd_1_prob[higher_seed_1_thru_16 - 1] if round == 1 else rd_2_and_after_prob[round - 2]

    rand_num = random.randint(1, 256)
    return higher_seed if (rand_num <= higher_seed_win_prob) else lower_seed

def decide_winners_for_round(matchup_list: List[int], round: int) -> List[int]:
    round_winners = []

    for i in range(1, len(matchup_list), 2):
        seeds_in_matchup = sorted([matchup_list[i - 1], matchup_list[i]])
        round_winners.append(decide_winner_for_game(seeds_in_matchup[0], seeds_in_matchup[1], round))

    return round_winners

def make_bracket():
    # Overall seeds in 2025 round 1: each pair represents a matchup
    matchup_list = [1, 64, 29, 33, 17, 45, 13, 49, 24, 42, 10, 53, 26, 38, 7, 60,
                    4, 61, 31, 36, 20, 46, 15, 52, 23, 43, 9,  55, 28, 37, 8, 59,
                    2, 63, 32, 35, 19, 48, 16, 51, 21, 44, 12, 56, 27, 39, 6, 57,
                    3, 62, 30, 34, 18, 47, 14, 50, 22, 41, 11, 54, 25, 40, 5, 58]

    bracket_seeds = []
    
    for round in range(1, 7):
        round_winners = decide_winners_for_round(matchup_list, round)
        bracket_seeds += round_winners        
        matchup_list = round_winners

    # we care about the team names, not the seeds
    return [teams_2025['abbr'][team - 1] for team in bracket_seeds]

if __name__ == "__main__":
    print(datetime.datetime.now())
    teams_2025 = pd.read_csv("./teams_2025.csv")

    all_brackets_list = []

    for i in range(2 ** 20):
        bracket = make_bracket()
        all_brackets_list.append(bracket)

    all_brackets_df = pd.DataFrame(all_brackets_list)
    all_brackets_df.to_csv("./brackets_2025.csv", index=False)
    print(datetime.datetime.now())