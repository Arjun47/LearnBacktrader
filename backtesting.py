import datetime
# from test_strategy import TestStrategy
from test_strategy2 import TestStrategy
# from test_strategy_sma import TestStrategy
import backtrader as bt

# tata_motors = "datas/TATAMOTORS.NS.csv"
au_small_finance_bank = "datas/au_small_finance_bank/AUBANK.NS.csv"
cerebro = bt.Cerebro()

cerebro.addstrategy(TestStrategy)

cerebro.broker.setcash(50000)
cerebro.broker.setcommission(commission=0.0011)
# cerebro.addsizer(bt.sizers.FixedSize, stake=10)
data = bt.feeds.YahooFinanceCSVData(dataname=au_small_finance_bank,
                                    fromdate=datetime.datetime(2022,4,1),
                                    todate=datetime.datetime.today(), reverse=False)

cerebro.adddata(data)

print(f"starting portfolio: {cerebro.broker.get_value()}")


cerebro.run()

print(f"Final Portfolio: {cerebro.broker.get_value()}")

cerebro.plot()