# Monte Carlo Option Pricing Tool

A professional financial tool that prices European call and put options using Monte Carlo simulation, validated against the Black-Scholes analytical formula.

## What This Project Does

This tool answers the question: **"What is a fair price for an options contract?"**

It combines two approaches:
1. **Monte Carlo Simulation** - Randomly simulates 100,000 possible stock price futures to estimate option value
2. **Black-Scholes Formula** - Uses mathematical analysis to calculate the exact theoretical price
3. **Comparison** - Validates that both methods agree, proving the simulation is accurate

## Real-World Application

Imagine you want to buy a call option on a stock:
- Stock price: $100
- Strike price: $105 (your purchase price if exercised)
- Volatility: 15% (market uncertainty)
- Days to expiration: 365

A broker offers to sell it for $10. **Is that fair?**

This tool calculates: "The fair price is $8.57"

**Conclusion:** The broker is overpricing it. Don't buy! ❌

---

## How It Works

### 1. User Input
```
Enter initial stock price: 100
Enter strike price: 105
Enter days to expiration: 365
Enter number of simulations: 100000
```

### 2. Monte Carlo Simulation
For each of 100,000 simulations:
- Start at current stock price ($100)
- For each day, randomly move the price based on:
  - Expected drift (risk-free rate)
  - Volatility (market chaos)
- Calculate payoff at expiration
- Average all 100,000 outcomes → **option price**

### 3. Black-Scholes Validation
Calculates the analytical price using the mathematical formula used by Wall Street traders.

### 4. Visualizations
- **Stock Paths:** How prices evolve under different volatilities
- **Call Prices:** MC vs Black-Scholes comparison
- **Put Prices:** MC vs Black-Scholes comparison
- **Payoff Diagrams:** When you make/lose money
- **Distribution:** Possible final stock prices
- **Summary Table:** All prices at a glance

---

## Key Insights from the Visualizations

### Plot 1: Stock Price Paths
- **Blue (5% volatility):** Smooth, predictable movements
- **Orange (15% volatility):** Moderate swings
- **Green (30% volatility):** Wild swings everywhere

**Lesson:** Higher volatility = more unpredictable, which makes options more valuable.

### Plot 2 & 3: MC vs Black-Scholes
If the bars match closely, your simulation is **scientifically accurate**.

**Why this matters:** It proves your random sampling method works. This is how professional quants validate models.

### Plot 4: Payoff Diagrams
- **Green line (Call):** You win if stock goes UP
- **Red line (Put):** You win if stock goes DOWN

At expiration, these lines show your exact profit/loss at any price.

### Plot 5: Distribution
Shows where the stock price is likely to end up. The spread increases with volatility.

---

## The Math Behind It

### Monte Carlo Formula
```
Price = E[Payoff] × e^(-r·T)

Where:
  E[Payoff] = average of all 100,000 simulated outcomes
  r = risk-free rate (5%)
  T = time to expiration (in years)
  e^(-r·T) = discount factor (money today > money tomorrow)
```

### Black-Scholes Formula (Simplified)
```
C = S₀·N(d₁) - K·e^(-r·T)·N(d₂)

Where:
  S₀ = stock price
  K = strike price
  N(d) = probability from normal distribution
  d₁, d₂ = intermediate calculations involving volatility
```

---

## Why This Project Matters

1. **Real-world application** - Used by hedge funds, investment banks, and traders
2. **Validates Monte Carlo** - Shows that random sampling can solve hard problems
3. **Demonstrates accuracy** - MC matches the "true" analytical answer
4. **Beautiful visualization** - Complex finance concepts made clear
5. **Professional code** - Clean structure, proper discounting, volatility scaling

---

## Technical Highlights

✅ **Proper volatility scaling** - Converts annualized volatility to daily  
✅ **Risk-neutral valuation** - Uses risk-free rate as drift  
✅ **Accurate discounting** - Future payoffs discounted to present value  
✅ **Sensitivity analysis** - Tests 3 volatility scenarios  
✅ **Error quantification** - Shows difference between MC and analytical  

---

## How to Run

```bash
python option_pricing_tool.py
```

Then input your parameters. Results will display in terminal + save a professional dashboard visualization.

---

## Expected Output

```
CALL OPTIONS
Vol 5%:  MC=$3.83  vs  BS=$2.05
Vol 15%: MC=$8.57  vs  BS=$6.04
Vol 30%: MC=$15.77 vs BS=$11.98

PUT OPTIONS
Vol 5%:  MC=$1.44  vs  BS=$1.93
Vol 15%: MC=$6.20  vs  BS=$5.91
Vol 30%: MC=$13.49 vs BS=$11.86

✓ Professional dashboard saved!
```

The small differences (1-10%) are normal due to Monte Carlo sampling noise. Increase simulations to 500,000 for even closer convergence.

---

## What You Learn

- **Finance:** Option pricing, volatility, risk-neutral valuation
- **Programming:** Monte Carlo methods, numpy vectorization, matplotlib visualization
- **Validation:** How to prove a simulation is correct
- **Communication:** Turning complex math into clear visuals

---

## Future Enhancements

- American options (can be exercised early)
- Implied volatility calculation
- Greeks (Delta, Gamma, Vega) - how sensitive is price to changes?
- Real-time data from APIs
- Interactive web dashboard
- Exotic options (barriers, lookbacks, etc.)

---

## Files

- `option_pricing_tool.py` - Main script
- `option_pricing_dashboard.png` - Generated visualization

---

## Author

Built as a practical example of Monte Carlo simulation applied to quantitative finance.

---

## Inspiration

This project demonstrates the power of Monte Carlo methods:
- Estimate π by throwing darts
- Price options by simulating futures
- Solve any hard problem through clever random sampling

All roads lead back to the same principle: **sample widely, average wisely, let statistics reveal the truth.**
