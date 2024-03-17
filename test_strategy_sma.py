import backtrader as bt

class TestStrategy(bt.Strategy):

    params = (
        ('maperiod', 15,),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

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
        self.log(f"Close, {self.dataclose[0]}")

        if self.order:
            return

        if not self.position:

            if self.dataclose[0] > self.sma[0]:
                # self.log(f"Buy Create, {self.dataclose[0]}")
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                # self.log(f"Sell Create {self.dataclose[0]}")
                self.order = self.sell()