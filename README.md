# PolyOrderbooks Backtest Strategies

Runnable strategy YAMLs for the
[`polyorderbooks-backtest`](https://github.com/polyorderbookslabs/polyorderbooks-backtest-python)
engine, which replays real L2 order-book history (250ms capture) from the
[PolyOrderbooks API](https://polyorderbooks.com) instead of approximating fills
from prices alone.

Everything here is a starting point, not a signal. Fills walk the visible
ladder, respect the `taker_fee` curve, model `trade_lag_seconds`, and settle
hold-to-expiry positions at the market's scheduled close against the recorded
winner.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

`POLYORDERBOOKS_API_KEY` comes from [polyorderbooks.com/signup](https://polyorderbooks.com/signup).

## Run one strategy

```bash
python run_one.py strategies/updown_momentum.yaml --top 20 --out results.csv
```

This uses the full CLI: `--market SLUG`, `--start`, `--end`, `--resolution`,
`--book-resolution`, `--top`, and `--out` are all available.

## Compare strategies

```bash
python compare.py
```

replays every strategy in `strategies/` over the same resolved-market set and
prints a per-strategy scorecard (trades, win rate, gross/net PnL, fees, average
return, Sharpe, max drawdown).

## Strategies

| File | Idea | Entry | Exit |
| --- | --- | --- | --- |
| `updown_momentum.yaml` | buy $100 of BTC Up when the Up side has climbed at least 3% over the trailing 2 minutes | `time ≥ 120s` AND `price_change Up ≥ +3% / 120s` | take profit at 0.75, stop loss at 0.20 |
| `breakout.yaml` | catch an early ETH Up breakout past 0.60 and hold to settlement | `time ≥ 60s` AND `price Up > 0.60` (within the first 8 minutes) | hold to expiry |
| `ladder_scalp.yaml` | scalp SOL Down with a tight trailing stop, re-entering up to 4 times, fills lagged 1 tick | `time ≥ 180s` | trailing stop 0.05 (activation 0.55) |

Outcome tokens that surface as `Yes`/`No` count as `Up`/`Down` for the side you
trade. If a market has no rows at the requested resolution the loader falls
back to coarser buckets (`60s` → `1m` → `5m` → `10m` → `1h`) so runs still
return results.

## History window

Free-tier API keys cover roughly the last three days of history, so these
strategies are designed for recent resolved markets (the default discovery
samples the most recent resolved markets matching the coin/type prefix). For
longer horizons, use a paid plan and pass `--start`/`--end` inside the covered
window.

## Community

- Add a strategy: open a PR with a YAML file plus a one-line description in
  the README table. Keep it runnable on the free tier where possible.
- Report issues in the [engine](https://github.com/polyorderbookslabs/polyorderbooks-backtest-python/issues) repo.

## License

MIT — see [LICENSE](LICENSE). Not affiliated with, endorsed by, or connected to Polymarket.