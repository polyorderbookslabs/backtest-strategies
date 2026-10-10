import sys
from pathlib import Path

import yaml
from polyorderbooks import PolyOrderbooksClient

from polyorderbooks_backtest.cli import strategy_from_yaml
from polyorderbooks_backtest.data import MarketBacktester, discover_markets
from polyorderbooks_backtest.metrics import summarize

DEFAULT_PATHS = [
    "strategies/updown_momentum.yaml",
    "strategies/breakout.yaml",
    "strategies/ladder_scalp.yaml",
]


def _load(path: str, strategy_from_yaml):
    with open(path, encoding="utf-8") as handle:
        return strategy_from_yaml(yaml.safe_load(handle))


def main(argv: list[str]) -> int:
    paths = argv or list(DEFAULT_PATHS)
    client = PolyOrderbooksClient()
    backtester = MarketBacktester(client)
    for path in paths:
        strategy = _load(path, strategy_from_yaml)
        markets = discover_markets(client, strategy, max_markets=strategy.sample_size)
        trades = []
        for market in markets:
            result = backtester.run_market(market, strategy)
            trades.extend(result.trades)
        summary = summarize(trades)
        print(f"{Path(path).name}: {len(trades)} trades over {len(markets)} markets")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))