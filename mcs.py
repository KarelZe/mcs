import math
from dataclasses import dataclass
from enum import Enum
from statistics import stdev

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotx
import numpy as np

text_color = "white"
plt.rcParams.update(
    {
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "axes.edgecolor": text_color,
        "legend.edgecolor": text_color,
    }
)


class CashflowType(Enum):
    """Enumeration for different types of cashflow events."""

    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


@dataclass
class CashflowEvent:
    """Represents a single cashflow event in the simulation.

    Attributes:
        year (int): The year of the event (0-indexed).
        amount (float): The monetary amount of the event.
        type (CashflowType): The type of cashflow (DEPOSIT or WITHDRAWAL).
        month (int, optional): The month of the event (0-11). Defaults to 0.
        description (str, optional): A brief description of the event. Defaults to "".
    """

    year: int
    amount: float
    type: CashflowType
    month: int = 0
    description: str = ""


@dataclass
class Asset:
    """Represents an investment asset with risk and return characteristics.

    Attributes:
        name (str): Name of the asset.
        mu (float): Annual arithmetic mean return (e.g., 0.05 for 5%).
        std (float): Annual standard deviation of returns.
        target_weight (float): Target allocation weight for this asset in the portfolio.
    """

    name: str
    mu: float
    std: float
    target_weight: float

    @property
    def mu_m(self) -> float:
        """float: Monthly arithmetic mean return."""
        return self.mu / 12

    @property
    def std_m(self) -> float:
        """float: Monthly standard deviation of returns."""
        return self.std / math.sqrt(12)


@dataclass
class Portfolio:
    """Represents a collection of assets with defined correlations.

    Attributes:
        assets (List[Asset]): List of assets in the portfolio.
        correlations (np.ndarray): Correlation matrix between assets.
    """

    assets: list[Asset]
    correlations: np.ndarray

    def __post_init__(self):
        """Normalizes asset weights and pre-computes the Cholesky matrix."""
        # Normalize weights
        total_weight = sum(a.target_weight for a in self.assets)
        for a in self.assets:
            a.target_weight /= total_weight

        # Pre-compute Cholesky for performance
        self._l_matrix = np.linalg.cholesky(self.correlations)

    @property
    def target_weights(self) -> np.ndarray:
        """np.ndarray: Vector of target weights for all assets."""
        return np.array([a.target_weight for a in self.assets])

    @property
    def mu_m_vector(self) -> np.ndarray:
        """np.ndarray: Vector of monthly mean returns for all assets."""
        return np.array([a.mu_m for a in self.assets])

    @property
    def std_m_vector(self) -> np.ndarray:
        """np.ndarray: Vector of monthly standard deviations for all assets."""
        return np.array([a.std_m for a in self.assets])

    def generate_returns(self) -> np.ndarray:
        """Generates correlated random monthly returns for all assets.

        Returns:
            np.ndarray: Vector of monthly returns.
        """
        z = np.random.normal(0, 1, len(self.assets))
        correlated_z = self._l_matrix @ z
        return self.mu_m_vector + self.std_m_vector * correlated_z


class SimulationEngine:
    """Core engine for running Monte Carlo simulations of portfolio growth.

    Attributes:
        portfolio (Portfolio): The portfolio to simulate.
        years (int): Number of years to simulate.
        rebalance_months (int, optional): Frequency of formal rebalancing in months. Defaults to 12.
        use_opportunistic_rebalance (bool, optional): Whether to use cashflows to
            correct weight imbalances. Defaults to True.
    """

    def __init__(
        self,
        portfolio: Portfolio,
        years: int,
        rebalance_months: int = 12,
        use_opportunistic_rebalance: bool = True,
    ):
        self.portfolio = portfolio
        self.years = years
        self.total_months = years * 12
        self.rebalance_months = rebalance_months
        self.use_opportunistic_rebalance = use_opportunistic_rebalance
        self.cashflows: list[CashflowEvent] = []

    def add_cashflow(self, event: CashflowEvent) -> None:
        """Adds a cashflow event to the simulation schedule.

        Args:
            event (CashflowEvent): The event to add.
        """
        self.cashflows.append(event)

    def _execute_transaction(
        self, asset_values: np.ndarray, amount: float
    ) -> np.ndarray:
        """Applies a cashflow to the portfolio, optionally using opportunistic rebalancing.

        Args:
            asset_values (np.ndarray): Current monetary value of each asset.
            amount (float): Net cashflow amount (positive for deposit, negative for withdrawal).

        Returns:
            np.ndarray: Updated monetary value of each asset.
        """
        total_val = np.sum(asset_values)
        new_total_val = total_val + amount

        if new_total_val <= 0:
            return np.zeros_like(asset_values)

        targets = self.portfolio.target_weights

        if self.use_opportunistic_rebalance:
            if amount > 0:
                # Direct deposits to assets that are furthest below their target weights
                needs = np.maximum(0.0, targets * new_total_val - asset_values)
                sum_needs = np.sum(needs)
                changes = (
                    (amount * needs / sum_needs)
                    if sum_needs > 0
                    else (amount * targets)
                )
                asset_values += changes
            else:
                # Withdraw from assets that are furthest above their target weights
                abs_amount = abs(amount)
                excesses = np.maximum(0.0, asset_values - targets * new_total_val)
                sum_excesses = np.sum(excesses)
                changes = (
                    (-abs_amount * excesses / sum_excesses)
                    if sum_excesses > 0
                    else (
                        amount
                        * (asset_values / total_val if total_val > 0 else targets)
                    )
                )
                asset_values += changes
        else:
            # Pro-rata allocation based on target weights
            asset_values += amount * targets

        return asset_values

    def run(self, num_iters: int = 1000) -> np.ndarray:
        """Runs the Monte Carlo simulation.

        Args:
            num_iters (int, optional): Number of simulation paths to generate. Defaults to 1000.

        Returns:
            np.ndarray: A 2D array of shape (num_iters, total_months) containing the
                total portfolio value over time for every path.
        """
        # Pre-calculate cashflow schedule for performance
        cf_schedule = np.zeros(self.total_months)
        for cf in self.cashflows:
            m = cf.year * 12 + cf.month
            if m < self.total_months:
                if cf.type == CashflowType.DEPOSIT:
                    cf_schedule[m] += cf.amount
                elif cf.type == CashflowType.WITHDRAWAL:
                    cf_schedule[m] -= cf.amount

        all_paths = np.zeros((num_iters, self.total_months))

        for i in range(num_iters):
            # Everything starts at zero; initial savings applied via cf_schedule[0]
            asset_values = np.zeros(len(self.portfolio.assets))

            for m in range(self.total_months):
                # Formal Rebalance
                if m > 0 and m % self.rebalance_months == 0:
                    total_val = np.sum(asset_values)
                    asset_values = total_val * self.portfolio.target_weights

                # Apply Cashflows (including initial savings at m=0)
                net_cf = cf_schedule[m]
                if net_cf != 0:
                    asset_values = self._execute_transaction(asset_values, net_cf)

                # Generate Returns
                asset_values *= 1 + self.portfolio.generate_returns()
                asset_values = np.maximum(asset_values, 0.0)

                all_paths[i, m] = np.sum(asset_values)

        return all_paths


if __name__ == "__main__":
    NUM_ITERS = 1000
    YEARS = 40

    # Parameters from Sketch.md
    assets = [Asset("Single Asset", mu=0.029, std=0.122, target_weight=1.0)]
    portfolio = Portfolio(assets, np.array([[1.0]]))

    # Initialize engine with opportunistic rebalancing enabled
    engine = SimulationEngine(
        portfolio,
        years=YEARS,
        use_opportunistic_rebalance=True,
    )

    # Initial savings deposit
    engine.add_cashflow(
        CashflowEvent(
            0, 1_000_000, CashflowType.DEPOSIT, month=0, description="Initial Savings"
        )
    )

    # 10 years of monthly deposits (50k / 12 each)
    for y in range(10):
        for m in range(12):
            engine.add_cashflow(
                CashflowEvent(y, 50_000 / 12, CashflowType.DEPOSIT, month=m)
            )

    # 30 years of monthly withdrawals (50k / 12 each)
    for y in range(10, 40):
        for m in range(12):
            engine.add_cashflow(
                CashflowEvent(y, 50_000 / 12, CashflowType.WITHDRAWAL, month=m)
            )

    print("Running simulation with Sketch.md parameters...")
    paths = engine.run(num_iters=NUM_ITERS)

    print(
        f"{'Year':<4} | {'10th Pct':>13} | {'50th Pct':>13} | {'Mean':>13}"
        f" | {'90th Pct':>13} | {'Std Dev':>13} | {'Success':>9} |"
    )
    for year in range(YEARS):
        if not (year % 5 == 0 or year == YEARS - 1):
            continue
        end_of_year = (year + 1) * 12 - 1
        dist = sorted(paths[:, end_of_year])

        q10 = round(dist[int(0.10 * NUM_ITERS)], -3)
        q50 = round(dist[int(0.50 * NUM_ITERS)], -3)
        q90 = round(dist[int(0.90 * NUM_ITERS)], -3)
        mean_val = round(np.mean(dist), -3)
        stdev_val = round(stdev(dist), -3)
        success_rate = np.mean(np.array(dist) > 0)

        print(
            f"{year + 1:<4} | {q10:>13,.0f} | {q50:>13,.0f} | {mean_val:>13,.0f}"
            f" | {q90:>13,.0f} | {stdev_val:>13,.0f} | {success_rate:>9.1%} |"
        )

    # Custom formatter for Y-axis (k and mio)
    def format_value(x, pos):
        if x >= 1_000_000:
            return f"{x * 1e-6:g}m"
        if x >= 1_000:
            return f"{x * 1e-3:g}k"
        return f"{x:g}"

    # Use matplotx for styling
    with plt.style.context(matplotx.styles.duftify(matplotx.styles.github["dark"])):
        plt.figure(figsize=(12, 6))
        time = np.linspace(0, YEARS, YEARS * 12)

        # Plot individual paths with transparency
        plt.plot(time, paths[:50].T, color="gray", alpha=0.2)

        # Plot percentiles
        plt.plot(
            time, np.percentile(paths, 50, axis=0), label="50th Pct", color="white"
        )
        plt.plot(
            time,
            np.percentile(paths, 10, axis=0),
            label="10th Pct",
            color="#ff3b30",
            linestyle="--",
        )
        plt.plot(
            time,
            np.percentile(paths, 90, axis=0),
            label="90th Pct",
            color="#4cd964",
            linestyle="--",
        )

        plt.title("Monte Carlo Simulation")
        plt.xlabel("Years")
        plt.ylabel("Portfolio Value")

        # Apply Y-axis formatter
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_value))
        matplotx.line_labels()  # Add labels at the end of lines
        # plt.grid(True, alpha=0.1)
        plt.savefig("oo_results.png", bbox_inches="tight")
        print("\nPlot saved to oo_results.png")
