import backtrader as bt
import pandas as pd
import numpy as np

class TestStrategy(bt.Strategy):

    params = (('ema_short', 9), ('ema_long', 30),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.ema_short = bt.indicators.ExponentialMovingAverage(self.datas[0].close, period=self.params.ema_short)
        self.ema_long = bt.indicators.ExponentialMovingAverage(self.datas[0].close, period=self.params.ema_long)

        self.last_signal = -1
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED Price: {order.executed.price}, Cost: {order.executed.value}, Comm: {order.executed.comm}")
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(f"SELL EXECUTED Price: {order.executed.price}, Cost: {order.executed.value}, Comm: {order.executed.comm}")
                pass
            self.bar_executed = len(self)
        elif order.status in [order.Cancelled, order.Margin, order.Rejected]:
            self.log("Order Cancelled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f"Operation Profit, GROSS: {trade.pnl}, NET: {trade.pnlcomm}")

    def next(self):

        if self.ema_short[0]  <= self.ema_long[0] and self.last_signal > 0:
            # If the 9-day EMA crosses above the 30-day EMA and the last signal was a sell, buy
            self.sell()
            self.last_signal = -1
            
        elif self.ema_short[0] >= self.ema_long[0] and self.last_signal < 0:
            # If the 9-day EMA crosses below the 30-day EMA and the last signal was a buy, sell
            self.buy()
            self.last_signal = 1