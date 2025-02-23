import yfinance as yf
import pandas as pd

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.object import BarData

# 1. 从 yfinance 获取数据
etf_symbols = [
        'XLK', # 科技行业
        'XLF', # 金融行业
        'XLV', # 医疗行业
        'XLE', # 能源行业
        'XLY', # 消费行业(非必须)
        'XLP', # 消费行业(日常)
        'XLI', # 工业行业
        'XLB', # 材料行业
        'XLU', # 公共事业
    ]
start_date = '2015-01-01'
end_date = '2026-01-01'

for symbol in etf_symbols:
    data = yf.download(symbol, start=start_date, end=end_date)

    # 2. 格式化数据为 vnpy 支持的格式
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # 选择需要的列
    data.index = pd.to_datetime(data.index).tz_localize("UTC")  # 确保日期是datetime格式

    # 3. 将数据导入到 vnpy 数据库
    # 获取数据库连接，假设你使用的是 SQLite 数据库
    db = get_database()  # 获取默认的数据库对象（会自动使用 SQLite）

    # 将数据插入到数据库
    bars = []
    for date, row in data.iterrows():
        bar = BarData(
            symbol=symbol,
            interval=Interval.DAILY,
            exchange=Exchange.NYSE,  # 设置交易所为 NASDAQ
            datetime=date,  # 设置数据时间
            open_price=row["Open"],
            high_price=row["High"],
            low_price=row["Low"],
            close_price=row["Close"],
            volume=row["Volume"],
            open_interest=0,  # 如果你没有open interest，填 0
            gateway_name = "Futu"
        )
        bars.append(bar)
    db.save_bar_data(bars)
    print(f"数据成功导入到数据库: {symbol}")
