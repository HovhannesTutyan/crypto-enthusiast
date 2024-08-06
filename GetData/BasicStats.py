from collections import Counter, defaultdict
from typing import List
import math, random

def dot(v, w):
    """v_1 * w_1 + v_2 * w_2 ... + v_n + w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_squares(v):
    """v_1 * v_1 + v_2 * v_2 ... + v_n * v_n"""
    return dot(v, v)

def vector_add(v, w):
    """adds two vectors componentwise"""
    return (v_i + w_i for v_i, w_i in zip(v, w))

def vector_subtract(v, w):
    """subtracts two vectors componentwise"""
    return (v_i - w_i for v_i, w_i in zip(v, w))

def scalar_multiply(c, v):
    return (c * v_i for v_i in v)

def mean(x: List[float])->float:
    return (sum(x) / len(x))

def median(v):
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2
    if n % 2 == 1:
        return (sorted_v[midpoint])
    else:
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2

def quantile(x, p):
    p_index = int(p*len(x))
    return sorted(x)[p_index]

def mode(x):
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]

def data_range(x: List[float])->float:
    """Difference of min and max data"""
    return (max(x) - min(x))

def de_mean(x: List[float]) -> List[float]:
    """Average of the data's absolute deviation about the central point"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x: List[float]) -> float:
    """average squared deviation from the mean"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n-1)

def standard_deviation(xs: List[float]) -> float:
    """square root of the variance"""
    return math.sqrt(variance(xs))

def interquartile_range(x):
    """half of the difference between third and first quartile"""
    return quantile(x, 0.75) - quantile(x, 0.25)

def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n-1)

def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0