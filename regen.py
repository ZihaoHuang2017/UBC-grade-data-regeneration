import math
from bisect import bisect_left
import typing
import copy

"""
Assume:
1. Distributions are normal, without skew (Allows for easy calculation of the stdev)
2. Distribution is capped from [lo, hi] (Allows for more accurate estimate)
3. All provided data are accurate
"""
NORMAL_SCORE_TABLE = [50, 55, 60, 64, 68, 72, 76, 80, 85, 90, 100]
ERFINV_25 = 0.674489750196  # Equal to erf^(-1)(0.25)


def get_table_index(score: int) -> int:
    # Returns where the score lies in the grade range.
    return bisect_left(NORMAL_SCORE_TABLE, score + 1)


def get_custom_capped_percentage(score, mean, stdev, lo, hi):
    # Returns the percentage of the student as a function.
    def normal_pdf(x):
        return (1 + math.erf((x - mean) / (math.sqrt(2) * stdev))) / 2

    if score == 100:
        return 1
    return (normal_pdf(score) - normal_pdf(lo)) / (normal_pdf(hi) - normal_pdf(lo))


def get_stdev(quantile_25, quantile_75):
    # Returns the persumed stdev since each quantile is approximately 0.675 stdevs
    # apart from the mean.
    return (quantile_75 - quantile_25) / (2 * ERFINV_25)


def get_to_be_filled_entries(arr, lo, hi) -> list[int]:
    # Returns a list of to-be-filled indexes.
    lo_index = get_table_index(lo)
    hi_index = get_table_index(hi)
    result = []
    for i in range(lo_index, hi_index + 1):
        if arr[i] == 0:
            result.append(i)
    return result


def get_range(index, lo, hi) -> tuple[int, int]:
    if index == 0:
        return lo, NORMAL_SCORE_TABLE[index]
    if index >= 10:
        return max(NORMAL_SCORE_TABLE[index], lo), min(100, hi)
    else:
        return max(NORMAL_SCORE_TABLE[index], lo), min(
            NORMAL_SCORE_TABLE[index + 1], hi
        )


def dhont(num_seats: int, votes: dict, lo, hi):
    # Returns the allocation of student according to d'Hondt algorithm,
    # but the lowest and highest entry are guaranteed a seat
    def preprocess(t_votes: dict, seats: dict):
        # Since there's guaranteed to be an entry for lo and hi bracket
        if get_table_index(lo) in seats:
            seats[get_table_index(lo)] += 1
            t_votes[get_table_index(lo)] = votes[get_table_index(lo)] / 2
        if get_table_index(hi) in seats:
            seats[get_table_index(hi)] += 1
            t_votes[get_table_index(hi)] = votes[get_table_index(hi)] / 2

    t_votes = copy.deepcopy(votes)
    seats = {}
    for key in votes:
        seats[key] = 0
    preprocess(t_votes, seats)
    while sum(seats.values()) < num_seats:
        next_seat = max(t_votes, key=t_votes.get)
        seats[next_seat] += 1
        t_votes[next_seat] = votes[next_seat] / (seats[next_seat] + 1)
    return seats


def fill_arr(arr, lo, hi, quantile_25, quantile_75, total_pop):
    result = copy.deepcopy(arr)
    to_be_filled_entries = get_to_be_filled_entries(arr, lo, hi)
    stdev = get_stdev(quantile_25, quantile_75)
    mean = (quantile_25 + quantile_75) / 2
    to_be_filled_pop = total_pop - sum(arr)
    alloc_dict = {}
    for i in to_be_filled_entries:
        range_lo, range_hi = get_range(i, lo, hi)
        alloc_dict[i] = get_custom_capped_percentage(range_hi, mean, stdev, lo, hi)
        -get_custom_capped_percentage(range_lo, mean, stdev, lo, hi)
    dhont_result = dhont(to_be_filled_pop, alloc_dict, lo, hi)
    for key in dhont_result:
        result[key] = dhont_result[key]
    assert sum(result) == total_pop
    return result


# [39, 0, 0, 0, 0, 6, 15, 25, 39, 59, 70]
# 75, 90, 98, 6, 263
INITIAL_ARR = [0] * 10 + [1]
QUANTILE_25, QUANTILE_75, HI, LO, TOTAL_POP = 69, 83, 90, 60, 13
print(fill_arr(INITIAL_ARR, LO, HI, QUANTILE_25, QUANTILE_75, TOTAL_POP))
