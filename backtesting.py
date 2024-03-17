import datetime
# from test_strategy import TestStrategy
from test_strategy_sma import TestStrategy
import backtrader as bt
import tkinter

tata_motors = "datas/TATAMOTORS.NS.csv"

cerebro = bt.Cerebro()

cerebro.addstrategy(TestStrategy)

cerebro.broker.setcash(50000)
cerebro.broker.setcommission(commission=0.0011)
# cerebro.addsizer(bt.sizers.FixedSize, stake=10)
data = bt.feeds.YahooFinanceCSVData(dataname=tata_motors,
                                    fromdate=datetime.datetime(2019,3,18),
                                    todate=datetime.datetime.today(), reverse=False)

cerebro.adddata(data)

print(f"starting portfolio: {cerebro.broker.get_value()}")


cerebro.run()

print(f"Final Portfolio: {cerebro.broker.get_value()}")

cerebro.plot()