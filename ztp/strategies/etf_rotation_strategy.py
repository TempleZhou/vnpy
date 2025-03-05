from datetime import datetime

from vnpy.trader.utility import ArrayManager, Interval
from vnpy.trader.object import TickData, BarData

from vnpy_portfoliostrategy import StrategyTemplate, StrategyEngine
from vnpy_portfoliostrategy.utility import PortfolioBarGenerator


class ETFRotationStrategy(StrategyTemplate):
    """美股 ETF 轮动策略"""

    author = "ZTP"

    momentum_period = 60
    rebalance_period = 5
    rsi_period = 50

    parameters = [
        "momentum_period",
        "rebalance_period",
        "rsi_period"
    ]
    variables = []

    def __init__(
        self,
        strategy_engine: StrategyEngine,
        strategy_name: str,
        vt_symbols: list[str],
        setting: dict
    ) -> None:
        """构造函数"""
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)

        self.targets: dict[str, int] = {}
        self.last_tick_time: datetime = None

        # 获取合约信息
        self.ams: dict[str, ArrayManager] = {}
        for vt_symbol in self.vt_symbols:
            self.ams[vt_symbol] = ArrayManager()
            self.targets[vt_symbol] = 0

        self.pbg = PortfolioBarGenerator(self.on_bars)

    def on_init(self) -> None:
        """策略初始化回调"""
        self.write_log("轮动策略初始化")

        self.load_bars(10)

    def on_start(self) -> None:
        """策略启动回调"""
        self.write_log("轮动策略启动")

    def on_stop(self) -> None:
        """策略停止回调"""
        self.write_log("轮动策略停止")

    def on_tick(self, tick: TickData) -> None:
        """行情推送回调"""
        self.pbg.update_tick(tick)

    def on_bars(self, bars: dict[str, BarData]) -> None:
        """日K线回调"""
        self.cancel_all()

        # 更新到缓存序列
        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            am.update_bar(bar)

        # rsi 记录
        rsi_list = []
        # 检查是否已经初始化
        for vt_symbol, bar in bars.items():
            am: ArrayManager = self.ams[vt_symbol]
            # 一般要100条数据才能完成初始化
            if not am.inited:
                return
            rsi = am.rsi(self.rsi_period)
            ma5 = am.sma(5)
            rsi_list.append((vt_symbol, rsi, bar.close_price))
        sorted_rsi_list = sorted(rsi_list, key=lambda x: x[1])
        for vt_symbol, rsi, closed_price in sorted_rsi_list[:3]:
            self.targets[vt_symbol] = 1
            self.buy(vt_symbol, closed_price, 100)

        # 推送界面更新
        self.put_event()
