# Monte Carlo Simulation

## Why

- Typically, you'd use a fixed withdrawal rate. It's good but still a point estimate. Most importantly they neglect that returns are uncertain in the future and don't tell us anything about future fluctuations of returns. Point estimates like these assume a simple, linear environment. (https://gerd-kommer.de/blog/monte-carlo-simulation-als-prognoseverfahren/)
- Looking ahead, the performance of investments is uncertain, and the longer the forecast horizon, the greater the range of possible final asset values. For portfolios that experience additions or withdrawals over time (which is, of course, the norm), this uncertainty has a particularly strong impact on returns and, consequently, on the final asset value. An MCS attempts to mathematically model this uncertainty for the investor’s informational purposes.
- We use MCS to find out, if:
    - our portfolio value is enough to maintain a certain life standard over a certain period.
    - for how long we have to save until we can retire.
- We have to differentiate *savings period* (deposit > withdrawals) and a *consumption period* (withdrawals > deposits)

## Notes

- Monte Carlo simulation (MCS) was invented in the late 1940s (post-WWII) by Stanislaw Ulam and John von Neumann for nuclear weapons research during the early Cold War.
- Monte Carlo simulations are a simple mathematical algorithm to find solutions for stochastic problems through random trials.
- In a MCS based on assumptions of expected return and volatility of a portfolio, the life expectancy of investors, and periodic portfolio deposits and withdrawals, the computer generates several hundred or thousands of trials (called iterations). We then sort results from best to worst. We can use this distribution to derive performance at certain confidence levels.
- What we'd like to find out is the *failure rate*, (German Pleitequote) Defined as 1 - Success rate. *success rate*: Percentage of cases that household net worth is sufficient to cover observation period.
- In the very best case, our portfolio would have a survival rate of 100 % and a failure rate of 0 %.
- There are three basic approaches to monte carlo sim: returns with random numbers under normal assumption (*the classical approach*), bootstrapping of historical returns, and historic traces with random starting points.
- For *bootstrapping with replacement* we'd use historical return (e.g., of the last 50 years) and draw them with replacement.
- For the fully *historical sequences simulation* we'd use long historical timeseries of returns (e.g., ranging from 1970 to present) and randomly sample starting points. If a sequence of returns, wouldn't be long enough, we wrap and sample the remaining historical sequence at the first available datapoint. This approach doesn't eliminate the reversion to the mean present in stock markets.
- The choice of the method also affects the predicted *failure rate*:
    - *classical MCS* typically leads to the highest failure rates
    - *bootstrapping with replacement MCS* leads to a middle failure rate among the three approaches
    - *historical sequences MCS* has the lowest failure rates, hence, most optimistic predictions.
- MCS is a means to manage sequence of returns risk. It means, that the specific order of fluctuating monthly and yearly returns during an observation period affect the total return and hence the total worth of the portfolio, if money is deposited or withdrawn from the portfolio. Only for portfolios without any withdrawals or deposits the sequence-of-return risk is irrelevant. For retirement accounts this is definitely not the case.
- Isn't there the 4 % rule? Yes, there is. It's overly optimistic these days and has tight assumptions (e.g., 50 % / 50 % portfolio composed of stocks and bonds, US historical data used for study must be considered an edge case). For details see: https://download.ssrn.com/2026/3/3/6336998.pdf.

## classical MCS

- *classical MCS* assumes normally distributed returns. Isn't the normality assumption flawed and overoptimistic, as it doesn't consider *fat tails* or *black swans*? For *black swans* see https://en.wikipedia.org/wiki/Black_swan_theory and books by Nasim Taleb.
- Research has shown that breaking the *normality assumption* would rather lead to more optimistic results and has hence adverse effects for our objective. For details see: https://www.kitces.com/blog/monte-carlo-analysis-risk-fat-tails-vs-safe-withdrawal-rates-rolling-historical-returns/


## Input parameters

We need to estimate:
1. existing net worth
2. savings and withdrawal rate
3. observation period (i.e, remaining life expectancy)
4. expected portfolio return and volatility

**remaining life expectancy:**

assume that the probability of a person to become older than a certain age is as low as 10 % or 20 %, not 50 % what typical calculators assume based on mean life expectancy.

**useful calculator:** https://www.7jahrelaenger.de/7jl/unsere-rechner/lebenserwartungsrechner


## Example to  reproduce

Sadly, Kommer doesn't publish his tools for MCS, but let me verify myself.

Example from https://gerd-kommer.de/blog/monte-carlo-simulation-als-prognoseverfahren/

*Parameters:*
- savings period: 10 years, withdrawal period 30 years
- deposits over course of 10 years: 50k, withdrawals in 10 years after that 
- remaining life expectancy of couple: 40 years
- real, arithmetic return of portfolio 2.9 % and std. dev. of returns 12.2 %. For *geometric returns* of different asset classes, see Kommer book p. 192. Arithmetic returns are roughly 1 % higher.
- consideration of inflation: not necessary, as we use *arithmetic, real returns*
- initial net worth: 1,000,000
- number of trials: unknown? But in book Kommer mentions 1,000 or 10,000 trials are mostly sufficient in financial context
- life expectancy. partners have an identical life expectancy: for examples, where partners have a different life expectancy, see Kommer book p. 189
- deposit, withdrawal and rebalance frequency: unknown. Probably yearly. Somewhere in his book Kommer writes that it makes calculations more precise but also more computationally expensive. Makes sense.

## withdrawals aren't static

- A household would typically adjust their withdrawal rate i.e., cut their spendings after a year of poor returns. Hence, in reality we'd often face situations with a *dynamic withdrawal rate*. (Kommer book; 2001) For *Plan B* ideas, see Kommer book.
- It might be wise to consider dynamic withdrawal rates. 

## considering inflation

## construction more risky portfolios

## Tasks


## Resources
- high-level overview https://www.gerd-kommer-invest.de/wp-content/uploads/Elitebrief-Monte-Carlo-Simulation-in-der-Finanzplanung.pdf
- more detailed overview how to calculate + cross-check for implementation. https://gerd-kommer.de/blog/monte-carlo-simulation-als-prognoseverfahren/. Seems very similar to the book "Souverän investieren vor und im Ruhestand"
- cuda + python-based monte carlo simulation: https://github.com/ToastierP/monte_carlo_sim/blob/main/MonteCarlo.py

## Mac Implementation

**torch:**

```python
import torch
device = torch.device("mps")
x = torch.ones(5, device=device)
```

**jax-metal:**

Project seems to be no longer actively maintained (see [discussion](https://github.com/jax-ml/jax/discussions/34648)).

**link:** https://developer.apple.com/metal/jax/

## geometric returns to arithmetic returns

Return Calculation: Geometric to ArithmeticTo convert a geometric return to an arithmetic return, you must account for volatility drag. The arithmetic mean is always higher than the geometric mean unless the volatility is zero.The standard approximation formula is:$$r_a \approx r_g + \frac{\sigma^2}{2}$$Calculation for Global StocksUsing a geometric return ($r_g$) of 6% and a typical global equity volatility ($\sigma$) of 18%:

Geometric Return ($r_g$): $0.06$
Variance ($\sigma^2$): $0.18^2 = 0.0324$
Adjustment: $0.0324 / 2 = 0.0162$ (or 1.62%)
Estimated Arithmetic Return: $0.06 + 0.0162 =$ 7.62%