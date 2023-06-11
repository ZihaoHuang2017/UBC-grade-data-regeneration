import math
from bisect import bisect_left
import typing
import copy

"""
Asssume:
1. Distributions are normal, without skew (Allows for easy calculation of the stdev)
2. Distribution is capped from [lo, hi] (Allows for more accurate estimate)
3. All provided data are accurate
"""
NORMAL_SCORE_TABLE = [50, 55, 60, 64, 68, 72, 76, 80, 85, 90, 100]
ERFINV_25 = 0.674489750196  # Equal to erf^(-1)(0.25)


def get_table_index(score: int) -> int:
    return bisect_left(NORMAL_SCORE_TABLE, score)


def get_custom_capped_percentage(mean, stdev, lo, hi):
    def normal_pdf(x):
        return 1 / 2 * (1 + math.erf((x - mean) / (math.sqrt(2) * stdev)))

    def percentage_calc(x):
        if x == 100:
            return 1
        return (normal_pdf(x) - normal_pdf(lo)) / (normal_pdf(hi) - normal_pdf(lo))

    return percentage_calc


def get_stdev(quantile_25, quantile_75):
    return (quantile_75 - quantile_25) / (2 * ERFINV_25)


def get_to_be_filled_entries(arr, lo, hi) -> list[int]:
    lo_index = get_table_index(lo)
    hi_index = get_table_index(hi)
    result = [0] * 11
    for i in range(lo_index, hi_index + 1):
        if arr[i] == 0:
            result[i] = 1
    return result


def get_range(index, lo, hi) -> tuple[int, int]:
    if index == 0:
        return lo, NORMAL_SCORE_TABLE[index]
    if index == 10:
        return max(NORMAL_SCORE_TABLE[index], lo), min(100, hi)
    else:
        return max(NORMAL_SCORE_TABLE[index], lo), min(
            NORMAL_SCORE_TABLE[index + 1], hi
        )


def fill_arr(arr, lo, hi, quantile_25, quantile_75, total_pop):
    result = copy.deepcopy(arr)
    to_be_filled_entries = get_to_be_filled_entries(arr, lo, hi)
    unfilled_relative_percentage = [0] * 11
    stdev = get_stdev(quantile_25, quantile_75)
    mean = (quantile_25 + quantile_75) / 2
    to_be_filled_pop = total_pop - sum(arr)
    print(to_be_filled_pop, mean, stdev)
    for index, item in enumerate(to_be_filled_entries):
        if item:
            range_lo, range_hi = get_range(index, lo, hi)
            unfilled_relative_percentage[index] = get_custom_capped_percentage(
                mean, stdev, lo, hi
            )(range_hi) - get_custom_capped_percentage(mean, stdev, lo, hi)(range_lo)
    
    total_weight_unfilled = sum(unfilled_relative_percentage)
    assert total_weight_unfilled <= 1
    for index, item in enumerate(unfilled_relative_percentage):
        if not result[index]:
            result[index] = item * to_be_filled_pop/total_weight_unfilled
        
    assert sum(result) == total_pop
    partial_sum = 0
    for i in result:
        if not isinstance(i, int):
            partial_sum += i
    assert abs(partial_sum - to_be_filled_pop) < 0.1
    return result

INITIAL_ARR = [0, 0, 0, 0, 0, 0, 0, 6, 8, 0, 7]
LO, HI = 61, 94
QUANTILE_25, QUANTILE_75 = 76, 88
TOTAL_POP = 34
print(fill_arr(INITIAL_ARR, LO, HI, QUANTILE_25, QUANTILE_75, TOTAL_POP))
