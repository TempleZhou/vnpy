from datetime import datetime
from importlib import reload

import vnpy_portfoliostrategy

from ztp.strategies.etf_rotation_strategy import ETFRotationStrategy

reload(vnpy_portfoliostrategy)

from vnpy_portfoliostrategy import BacktestingEngine
from vnpy.trader.constant import Interval

if __name__ == '__main__':
    symbols = ['XLK.NYSE',
               'XLF.NYSE',
               'XLV.NYSE',
               'XLE.NYSE',
               'XLY.NYSE',
               'XLP.NYSE',
               'XLI.NYSE',
               'XLB.NYSE',
               'XLU.NYSE']
    rate = 2 / 10000
    slippage = 0
    size = 1
    pricetick = 0.001

    rates = {symbol: rate for symbol in symbols}
    slippages = {symbol: slippage for symbol in symbols}
    sizes = {symbol: size for symbol in symbols}
    priceticks = {symbol: pricetick for symbol in symbols}

    engine = BacktestingEngine()

    engine.set_parameters(
        vt_symbols=symbols,
        interval=Interval.DAILY,
        start=datetime(2019, 1, 1),
        end=datetime(2022, 4, 30),
        # 每种vt_symbol的手续费率
        rates=rates,
        # 每种vt_symbol的滑点
        slippages=slippages,
        # 每种vt_symbol每手volume等于多少数量，实际下单数量=volume*size
        sizes=sizes,
        # 每种vt_symbol的价格数值格式，例如 1=取整，0.01=保留两位小数
        priceticks=priceticks,
        capital=1_000_000,
    )

    setting = {
    }
    engine.add_strategy(ETFRotationStrategy, setting)

    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    engine.calculate_statistics()
    aaa = engine.get_all_trades()
    print(aaa)
    engine.show_chart()
