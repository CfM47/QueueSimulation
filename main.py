from numpy import exp, random

from TandemSystem import TandemSystem
from stats import statistics, graphic_total_times, bootstrap_total_time_median, bootstrap_total_time_mean


def intensity_function(t: int):
    return 2 * exp(-t/240)

max_lambda = 2

def first_server_generator():
    result =  random.normal(0.5, 0.25)
    return result if result > 0 else 0.005

def second_server_generator():
    result =  random.normal(0.6, 0.25)
    return result if result > 0 else 0.005

total_time = 480 # minutes of 8-hour work day

simulation = TandemSystem(
    intensity_function,
    max_lambda,
    [first_server_generator, second_server_generator],
    total_time
)

simulation.run_simulation()
stats = statistics(simulation)
print(stats['total_system_times'])
graphic_total_times(stats)
bootstrap_total_time_mean(stats)
bootstrap_total_time_median(stats)
