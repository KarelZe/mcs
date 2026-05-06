from statistics import stdev
import random

NUM_ITERS = 1_000

REMAINING_LIFE_EXPECTANCY = 40
SAVINGS_PERIOD = 10
WITHDRAWAL_PERIOD = REMAINING_LIFE_EXPECTANCY - SAVINGS_PERIOD

INITIAL_SAVINGS = 1_000_000
ANNUAL_DEPOSIT = 50_000
ANNUAL_WITHDRAWAL = 50_000

MU = 0.029  # arithmetic, real return
STD = 0.122  # std. deviations

# core loop.
paths = []
for i in range(NUM_ITERS):
    path: list[float] = []
    savings = INITIAL_SAVINGS
    for j in range(SAVINGS_PERIOD):
        # assumption is we deposit first e.g., on January 1st, then get return.
        savings += ANNUAL_DEPOSIT
        savings *= 1 + random.gauss(MU, STD)
        # if savings < 0, we are broke.
        savings = max(savings, 0)
        path.append(savings)
    for j in range(WITHDRAWAL_PERIOD):
        # assumption is we withdraw first, then get return.
        savings -= ANNUAL_WITHDRAWAL
        savings *= 1 + random.gauss(MU, STD)
        # if savings < 0, we are broke.
        savings = max(savings, 0)
        path.append(savings)

    paths.append(path)

print(
    f"{'Year':<4} | {'10th Percentile':<15} | {'50th Percentile':<15} | {'Mean':<15} | {'90th Percentile':<15} | {'Std. Deviation':<15} | {'Success Rate':<15} |"
)
for year in range(len(paths[0])):
    # print every 5 years, and the last year, as in book.
    if not (year % 5 == 0 or year == len(paths[0]) - 1):
        continue
    distribution_year = sorted(path[year] for path in paths)

    # calculate distribution
    quantile_10, quantile_50, quantile_90 = (
        distribution_year[int(0.1 * NUM_ITERS)],
        distribution_year[int(0.5 * NUM_ITERS)],
        distribution_year[int(0.9 * NUM_ITERS)],
    )
    mean = sum(distribution_year) / NUM_ITERS

    # round to thousands, as in book
    quantile_10 = round(quantile_10, -3)
    quantile_50 = round(quantile_50, -3)
    quantile_90 = round(quantile_90, -3)
    mean = round(mean, -3)
    stdev_value = round(stdev(distribution_year), -3)
    success_rate = (NUM_ITERS - distribution_year.count(0)) / NUM_ITERS

    print(
        f"{year:<4} | {quantile_10:>15,.2f} | {quantile_50:>15,.2f} | {mean:>15,.2f} | {quantile_90:>15,.2f} | {stdev_value:>15,.2f} | {success_rate:>15,.2f} |"
    )
