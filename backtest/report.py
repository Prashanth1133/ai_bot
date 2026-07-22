class BacktestReport:

    def generate(

        self,

        metrics,

    ):

        print()

        print("=" * 60)

        print("BACKTEST REPORT")

        print("=" * 60)

        print(metrics.total_return)

        print(metrics.max_drawdown)

        print(metrics.win_rate)

        print(metrics.profit_factor)

        print(metrics.sharpe)