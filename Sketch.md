# Monte Carlo Simulation

## Why

- Typically, you'd use a fixed withdrawal rate. It's good but still an point estimate. Most importantly they neglect, that returns are uncertain in the future and don't tell us anything about future fluctuations of returns. Point estimates like these assume a simple, linear environment. (https://gerd-kommer.de/blog/monte-carlo-simulation-als-prognoseverfahren/)

## Notes

- Monte Carlo simulation (MCS) was invented for the development of nuclear weapons during World War II.
- Monte Carlo simulations are a simple mathematical algorithm to find solutions for stochastic problems through random trials.
- In a MCS based on assumptions of expected return and volatility of a portfolio, the life expectancy of investors and periodic portfolio deposits and withdrawals the computer generates several hundred or thousand of trials (called iterations). We finally sort the results worst. We can use this distribution to derive performance at certain confidence levels.
- There are three basic approaches to monte carlo sim: returns with random numbers under normal assumption, bootstrapping of historical returns, and historic traces with random starting points.
- MCS is a means to manage sequence of returns risk. It means, that the specific order of fluctuating monthly and yearly returns during an observation period affect the total return and hence the total worth of the portfolio, if money is deposited or withdrawn from the portfolio. Only for portfolios without any withdrawals or deposits the sequence-of-return risk is irrelevant. For retirement accounts this is definitely not the case.

**remaining life expectancy:**

assume that the probability of person to become older than a certain age is as low as 10 % or 20 %, not 50 % percent what typical calculators assume based on mean life expectancy.

**useful calculator:** https://www.7jahrelaenger.de/7jl/unsere-rechner/lebenserwartungsrechner

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

