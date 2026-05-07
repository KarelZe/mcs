# mcs
A Monte Carlo simulation for your securities account. Die with zero.

## Features

- **Multi-Asset Support**: Model portfolios with multiple assets, each with its own risk/return profile and target weight.
- **Intelligent Cashflow Allocation**: Deposits and withdrawals can be automatically allocated to minimize tracking error from target weights (opportunistic rebalancing).
- **Periodic Rebalancing**: Automated portfolio rebalancing at fixed intervals (e.g., annually).
- **Flexible Cashflows**: Support for scheduled lump sums, changing savings rates, and dynamic withdrawal guardrails.
- **Success Rate Analysis**: Calculates the probability of portfolio survival over long horizons.

## Usage

Configure your parameters in `mcs.py` and run:

```bash
python3 mcs.py
```
