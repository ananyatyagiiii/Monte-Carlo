import numpy as np
 
from option_pricing_tool import (
    black_scholes_call,
    black_scholes_put,
    calculate_option_price,
    simulate_terminal_prices,
)
 
 
# Shared parameters kept small so the test suite runs fast in CI
DAYS = 30
SIMS = 300
R = 0.05
T = DAYS / 365
 
 
class TestBlackScholes:
    """Tests for the analytical Black-Scholes formulas."""
 
    def test_call_price_is_non_negative(self):
        price = black_scholes_call(100, 100, T, R, 0.20)
        assert price >= 0
 
    def test_put_price_is_non_negative(self):
        price = black_scholes_put(100, 100, T, R, 0.20)
        assert price >= 0
 
    def test_call_falls_as_strike_rises(self):
        """A call gets cheaper the higher the strike."""
        cheap_strike = black_scholes_call(100, 90, T, R, 0.20)
        pricey_strike = black_scholes_call(100, 110, T, R, 0.20)
        assert cheap_strike > pricey_strike
 
    def test_put_rises_as_strike_rises(self):
        """A put gets more expensive the higher the strike."""
        low_strike = black_scholes_put(100, 90, T, R, 0.20)
        high_strike = black_scholes_put(100, 110, T, R, 0.20)
        assert high_strike > low_strike
 
    def test_call_rises_with_volatility(self):
        """More volatility means more optionality, so a higher price."""
        calm = black_scholes_call(100, 100, T, R, 0.05)
        wild = black_scholes_call(100, 100, T, R, 0.40)
        assert wild > calm
 
    def test_put_call_parity(self):
        """C - P should equal S - K*exp(-rT)."""
        S, K = 100, 105
        call = black_scholes_call(S, K, T, R, 0.20)
        put = black_scholes_put(S, K, T, R, 0.20)
 
        assert abs((call - put) - (S - K * np.exp(-R * T))) < 1e-6
 
    def test_deep_in_the_money_call_approaches_intrinsic(self):
        """A deep ITM call is worth roughly its intrinsic value."""
        price = black_scholes_call(200, 100, T, R, 0.20)
        intrinsic = 200 - 100 * np.exp(-R * T)
        assert abs(price - intrinsic) < 0.01
 
 
class TestMonteCarlo:
    """Tests for the Monte Carlo pricing engine."""
 
    def test_returns_price_and_path(self):
        result = calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T)
        assert len(result) == 2
 
        price, path = result
        assert isinstance(price, float) or np.isscalar(price)
        assert len(path) == DAYS + 1
 
    def test_path_starts_at_initial_price(self):
        _, path = calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T)
        assert path[0] == 100
 
    def test_call_price_is_non_negative(self):
        price, _ = calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T,
                                          option_type='call')
        assert price >= 0
 
    def test_put_price_is_non_negative(self):
        price, _ = calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T,
                                          option_type='put')
        assert price >= 0
 
    def test_itm_call_beats_otm_call(self):
        """Strike 90 should price above strike 130 for a $100 stock."""
        np.random.seed(0)
        itm, _ = calculate_option_price(100, 90, 0.20, DAYS, SIMS, R, T,
                                        option_type='call')
        np.random.seed(0)
        otm, _ = calculate_option_price(100, 130, 0.20, DAYS, SIMS, R, T,
                                        option_type='call')
        assert itm > otm
 
    def test_itm_put_beats_otm_put(self):
        """Strike 130 should price above strike 70 for a $100 stock."""
        np.random.seed(0)
        itm, _ = calculate_option_price(100, 130, 0.20, DAYS, SIMS, R, T,
                                        option_type='put')
        np.random.seed(0)
        otm, _ = calculate_option_price(100, 70, 0.20, DAYS, SIMS, R, T,
                                        option_type='put')
        assert itm > otm
 
    def test_deep_otm_call_is_worthless(self):
        """A strike far above any reachable price should price near zero."""
        price, _ = calculate_option_price(100, 1000, 0.20, DAYS, SIMS, R, T,
                                          option_type='call')
        assert price == 0
 
    def test_invalid_option_type_raises(self):
        import pytest
        with pytest.raises(ValueError):
            calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T,
                                   option_type='banana')
 
    def test_result_is_reproducible_with_seed(self):
        """Same seed, same inputs, same price."""
        np.random.seed(123)
        first, _ = calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T)
        np.random.seed(123)
        second, _ = calculate_option_price(100, 105, 0.20, DAYS, SIMS, R, T)
        assert first == second
 
 
class TestMonteCarloVsAnalytical:
    """Sanity checks that MC lands in the same ballpark as Black-Scholes."""
 
    def test_call_is_within_an_order_of_magnitude(self):
        np.random.seed(42)
        mc, _ = calculate_option_price(100, 100, 0.20, DAYS, 2000, R, T,
                                       option_type='call')
        bs = black_scholes_call(100, 100, T, R, 0.20)
 
        # Now that the step size matches T, MC should track BS closely.
        # 15% allows for sampling noise (worst observed: 6.4% over 12 runs).
        assert abs(mc - bs) / bs < 0.15
 
    def test_put_is_within_an_order_of_magnitude(self):
        np.random.seed(42)
        mc, _ = calculate_option_price(100, 100, 0.20, DAYS, 2000, R, T,
                                       option_type='put')
        bs = black_scholes_put(100, 100, T, R, 0.20)
 
        assert abs(mc - bs) / bs < 0.15


class TestTerminalDistribution:
    """The terminal price should be exactly lognormal under risk-neutral
    GBM: log(S_T) ~ Normal(log(S0) + (r - 0.5*sigma**2)*T, sigma**2*T).
    These check that distribution directly, rather than only checking
    that a downstream option price comes out close to Black-Scholes."""

    def test_log_price_mean_matches_gbm_drift(self):
        np.random.seed(1)
        s0, sigma = 100, 0.25
        final_prices = simulate_terminal_prices(s0, sigma, 200_000, R, T)
        expected_mean = np.log(s0) + (R - 0.5 * sigma**2) * T
        assert abs(np.mean(np.log(final_prices)) - expected_mean) < 0.01

    def test_log_price_std_matches_gbm_variance(self):
        np.random.seed(1)
        s0, sigma = 100, 0.25
        final_prices = simulate_terminal_prices(s0, sigma, 200_000, R, T)
        expected_std = sigma * np.sqrt(T)
        assert abs(np.std(np.log(final_prices)) - expected_std) < 0.01

    def test_terminal_price_is_never_negative(self):
        """Unlike stepping the simple return as normal (price *= 1 + N(...)),
        exact GBM can't produce a negative price."""
        np.random.seed(2)
        final_prices = simulate_terminal_prices(100, 0.80, 100_000, R, T)
        assert np.all(final_prices > 0)
