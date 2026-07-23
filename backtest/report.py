class BacktestReport:


    def generate(

        self,
        metrics

    ):


        print()

        print("="*60)

        print("BACKTEST REPORT")

        print("="*60)


        print(

            "Return :",

            metrics.total_return

        )


        print(

            "Drawdown :",

            metrics.max_drawdown

        )


        print(

            "Win Rate :",

            metrics.win_rate

        )


        print(

            "Profit Factor :",

            metrics.profit_factor

        )


        print(

            "Sharpe Ratio :",

            metrics.sharpe

        )


        print("="*60)


        return {

            "return":

            metrics.total_return,

            "drawdown":

            metrics.max_drawdown,

            "win_rate":

            metrics.win_rate,

            "profit_factor":

            metrics.profit_factor,

            "sharpe":

            metrics.sharpe

        }