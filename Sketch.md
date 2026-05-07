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
- From Alexander Carol for VaR: But in the historical VaR model, simulations of portfolio returns are based on a set of historical asset or risk factor returns. Historical VaR can be a very powerful tool for forecasting extreme losses, but a significant challenge to implementing an historical VaR model is the derivation of an empirical portfolio returns distribution that captures the tails of the distribution adequately. The aim of kernel fitting is to derive a smooth curve from a random sample that provides the best possible representation of the probability density of the random variable. In other words, kernel fitting is a way to infer the population density from an empirical density function.


## classical MCS

** from kommer:**

- *classical MCS* assumes normally distributed returns. Isn't the normality assumption flawed and overoptimistic, as it doesn't consider *fat tails* or *black swans*? For *black swans* see https://en.wikipedia.org/wiki/Black_swan_theory and books by Nasim Taleb.
- Research has shown that breaking the *normality assumption* would rather lead to more optimistic results and has hence adverse effects for our objective. For details see: https://www.kitces.com/blog/monte-carlo-analysis-risk-fat-tails-vs-safe-withdrawal-rates-rolling-historical-returns/

**but:**

Came to my mind while reading I.3.3.12 Kernels in Alexander.

In reality, markets  have "Fat Tails" (Kurtosis). 
   * The Normal Model: Predicts that a "6-sigma" event (like the
     2008 crash) should happen once every few billion years.
   * The Reality: These events happen once or twice a decade.
   * The Alexander Point: If you use a historical sample directly,
     it’s too "jagged." If you use a Normal curve, it’s too
     "thin." Kernel fitting (KDE) is the middle ground that
     creates a smooth, continuous distribution that actually
     respects those historical extremes.

How to model fat tails:

   1. The "Easy" Math Fix (Student's t-distribution): Instead of
      Normal, use a Student’s t-distribution with low "degrees of
      freedom" (e.g., 3 to 5). This automatically adds the "fat
      tails" Alexander is worried about without needing a massive
      historical dataset.
   2. The Alexander Fix (KDE Bootstrapping): If you have a file of
      historical returns for your assets, we can replace
      np.random.normal with a Scipy gaussian_kde sampler. This
      will "infer the population density" from your data as she
      describes.

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
- deposits over course of 10 years: 50k per year, withdrawals in 10 years after that  
- remaining life expectancy of couple: 40 years
- real, arithmetic return of portfolio 2.9 % and std. dev. of returns 12.2 %. For *geometric returns* of different asset classes, see Kommer book p. 192. Arithmetic returns are roughly 1 % higher.
- consideration of inflation: not necessary, as we use *arithmetic, real returns*
- initial net worth: 1,000,000
- number of trials: unknown? But in book Kommer mentions 1,000 or 10,000 trials are mostly sufficient in financial context
- life expectancy. partners have an identical life expectancy: for examples, where partners have a different life expectancy, see Kommer book p. 189
- deposit, withdrawal and rebalance frequency: unknown. Probably yearly, as all numbers are reported annually. Somewhere in his book Kommer writes that it makes calculations more precise but also more computationally expensive. Makes sense. It's also unclear when withdrawals are done, at beginning of year, end of year, or every month?
- Beginning-of-year withdrawal is the conservative choice — you reduce the base before it compounds, which slightly lowers your median outcome and raises the failure rate End-of-year withdrawal would give slightly more optimistic numbers. 

## withdrawals aren't static

- A household would typically adjust their withdrawal rate i.e., cut their spendings after a year of poor returns. Hence, in reality we'd often face situations with a *dynamic withdrawal rate*. (Kommer book; 2001) For *Plan B* ideas, see Kommer book.
- It might be wise to consider dynamic withdrawal rates. 

## geometrics vs. arithmetic returns

Arithmetic returns (mean annual return) should be used as inputs for Monte Carlo simulations, not geometric returns (CAGR), to avoid double-counting "volatility drag". The simulation randomizes yearly returns, and the compounding effect naturally generates the necessary volatility, reducing the effective return from the arithmetic average to a lower, more realistic compounded result.Why Arithmetic: It represents the expected return for any single future year. (https://support.planwithvoyant.com/hc/en-us/articles/40766720226971-Understanding-Arithmetic-vs-Geometric-Mean-US#:~:text=For%20Monte%20Carlo%20simulations%2C%20where,between%20arithmetic%20and%20geometric%20values.) Why Not Geometric: It already accounts for past volatility (compounding), which the simulation will calculate again, resulting in artificially low projections.Key Consideration: The simulation handles sequence-of-returns risk, meaning it models how early losses affect long-term portfolio survival.


## considering inflation

## construction more risky portfolios

## Tasks

## a word about pseudo, random numbers

see chapter I.5.7.1 Random Numbers in Alexander. Instead of Mersenne-Twister, we use PCG64 rng algorithm, which is faster. Marsenne-Twister has a high periodicity -> long cycle before the random sequence repeats For MT the period is $2^{19937}-1$, which is massive and more than enough for most portfolio simulations.

# Pitfalls in Monte Carlo simulation

see handbook on mcs (pp. 45)

## Background on Sequence-of-Return risk

1. The "Academic Gold Standard"
  "The Calculus of Retirement Income" by Moshe Milevsky
   * The Vibe: This is the most mathematically rigorous book on
     the list. If you like Carol Alexander’s work, you will
     appreciate Milevsky. 
   * Why it’s great: He treats retirement not as a "savings"
     problem but as an "actuarial" problem. He uses stochastic
     calculus to explain why the variance of returns during the
     withdrawal phase is fundamentally different from the variance
     during the accumulation phase.
2. The "Behavioral & Historical" Perspective
  "The Four Pillars of Investing" by William Bernstein
   * The Vibe: Historical, narrative-driven, but backed by deep
     data.
   * Why it’s great: Bernstein explains that SoRR is essentially a
     "collision" between market volatility and human mortality. He
     provides the historical context of "lost decades" (like
     1929-1939 or 2000-2010) to show exactly how a bad sequence
     destroys a life standard.
3. The "Professional/Institutional" View
  "Asset Management: A Systematic Approach to Factor Investing" by
  Andrew Ang
   * The Vibe: Institutional-grade textbook.
   * Why it’s great: Chapter 18 (on "Liquidating Portfolios")
     provides a very high-level mathematical treatment of
     decumulation. It’s excellent if you want to understand how
     institutions manage the "sequence risk" of pension funds,
     which is exactly what an individual retirement portfolio is.


## Resources
- high-level overview https://www.gerd-kommer-invest.de/wp-content/uploads/Elitebrief-Monte-Carlo-Simulation-in-der-Finanzplanung.pdf
- more detailed overview how to calculate + cross-check for implementation. https://gerd-kommer.de/blog/monte-carlo-simulation-als-prognoseverfahren/. Seems very similar to the book "Souverän investieren vor und im Ruhestand"
- cuda + python-based monte carlo simulation: https://github.com/ToastierP/monte_carlo_sim/blob/main/MonteCarlo.py
- useful book: Handbook in Monte Carlo Simulation: Applications in Financial Engineering, Risk Management, and Economics
- most relevant book: Market Risk Analysis Volume I: Quantitative Methods in Finance
- monte carlo methods in financial engineering https://www.bauer.uh.edu/spirrong/Monte_Carlo_Methods_In_Financial_Enginee.pdf


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

**pure python:**

probably enough to do in pure python, as runtime doesn't matter match and calculation is fairly fast.

## geometric returns to arithmetic returns

Return Calculation: Geometric to ArithmeticTo convert a geometric return to an arithmetic return, you must account for volatility drag. The arithmetic mean is always higher than the geometric mean unless the volatility is zero.The standard approximation formula is:$$r_a \approx r_g + \frac{\sigma^2}{2}$$Calculation for Global StocksUsing a geometric return ($r_g$) of 6% and a typical global equity volatility ($\sigma$) of 18%:

Geometric Return ($r_g$): $0.06$
Variance ($\sigma^2$): $0.18^2 = 0.0324$
Adjustment: $0.0324 / 2 = 0.0162$ (or 1.62%)
Estimated Arithmetic Return: $0.06 + 0.0162 =$ 7.62%

## Generating Time Series of Lognormal Asset Prices
 
(from Alexander)

In this subsection we describe how to simulate a time series of asset prices that follow a geometric Brownian motion,

$$
\frac{d S(t)}{S(t)}=\mu d t+\sigma d W(t) .
$$

Geometric Brownian motion was introduced in Section I.1.4.5, and we derived the discrete time equivalent of geometric Brownian motion in Section I.3.7.3. Using Itô's lemma we showed that the log return, which is the first difference in the log prices, is normally and independently distributed with mean $\mu-\frac{1}{2} \sigma^2$ and variance $\sigma^2$.

Now suppose we fix $\mu$ and $\sigma$ and simulate a sequence $\left\{x_1, x_2, \ldots, x_T\right\}$, where each $x_i$ has mean $\alpha=\mu-\frac{1}{2} \sigma^2$ and variance $\sigma$ as described in the previous section. In a risk neutral world the drift $\mu$ is equal to the risk free rate $r,{ }^{33}$ so (I.5.46) becomes

$$
x_t=z_t \sigma+r-\frac{1}{2} \sigma^2,
$$

where $\left\{z_1, z_2, \ldots, z_T\right\}$ are independent standard normal simulations. We suppose that the simulation $\left\{x_1, x_2, \ldots, x_T\right\}$ represents a set of $\log$ returns, i.e.

$$
x_1=\ln \left(S_1 / S_0\right), \quad x_2=\ln \left(S_2 / S_1\right), \ldots .
$$

for some sequence of asset prices $\left\{S_0, S_1, S_2, \ldots, S_T\right\}$ and for a fixed $S_0$ which is the current price of the asset. Given a simulation $\left\{x_1, x_2, \ldots, x_T\right\}$ and given $S_0$, we use $x_1$ to obtain the next price as $S_1=\exp \left(x_1\right) S_0$. More generally the consecutive prices of the assets are given by

$$
S_t=\exp \left(x_t\right) S_{t-1} .
$$ƒRes

So this is how we simulate prices that follow a geometric Brownian motion.
To illustrate (I.5.48) we generate some possible price paths for an asset that follows a geometric Brownian motion with drift $5 \%$ and volatility $20 \%$. Suppose we generate the paths in daily increments over 1 year. Then we must use the daily drift $0.05 / 365=0.000137$ and the daily standard deviation $0.2 / \sqrt{ } 365=0.010468$ in the simulation.

## Simulations on a System of Two Correlated Normal Returns

Correlated simulations are necessary for computing the Monte Carlo VaR of a portfolio, and we shall be drawing on the techniques described in this section very frequently in Volume IV. Suppose we wish to generate two sequences of random draws that represent the returns on correlated assets. For simplicity we shall again assume that each asset's returns are normally distributed with means $\mu_1$ and $\mu_2$, standard deviations $\sigma_1$ and $\sigma_2$ and correlation $\varrho$. We first write down the covariance matrix,

$$
\mathbf{V}=\left(\begin{array}{cc}
\sigma_1^2 & \varrho \sigma_1 \sigma_2 \\
\varrho \sigma_1 \sigma_2 & \sigma_2^2
\end{array}\right),
$$

then we find its Cholesky matrix $\mathbf{C}$, i.e. the lower triangular matrix such that $\mathbf{V}=\mathbf{C C}^{\prime}{ }^{35}$ Now we take two independent standard normal simulations, $\mathrm{z}_1$ and $\mathrm{z}_2$, one for each asset and set

$$
\binom{x_1}{x_2}=\mathbf{C}\binom{\mathrm{z}_1}{\mathrm{z}_2} .
$$


Then $x_1$ and $x_2$ will have the correct standard deviations and correlation, because taking variance of the above gives

$$
V\binom{x_1}{x_2}=C V\binom{z_1}{z_2} C^{\prime}=C^{\prime} C^{\prime}=V .
$$

Finally, adding $\mu_1$ to $x_1$ and $\mu_2$ to $x_2$ gives the required result.