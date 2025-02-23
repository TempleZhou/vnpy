# 定义要回测的ETF列表
import os
import yfinance as yf
import pandas as pd

if __name__ == '__main__':

    etf_symbols = [
        'XLK', # 科技行业
        'XLF', # 金融行业
        'XLV', # 医疗行业
        'XLE', # 能源行业
        'XLY', # 消费行业 非必须
        'XLP', # 消费行业 日常
        'XLI', # 工业行业
        'XLB', # 材料行业
        'XLU', # 公共事业
    ]

    # 加载数据
    data_folder = 'data'
    start_date='2015-01-01'
    end_date='2025-12-31'
    # 加载数据
    for symbol in etf_symbols:
        # 生成缓存文件的文件名
        cache_filename = os.path.join(data_folder, f'{symbol}_{start_date}_{end_date}.csv')
        # 检查缓存文件是否存在
        if os.path.exists(cache_filename):
            # 如果缓存文件存在，从文件中加载数据
            data = pd.read_csv(cache_filename)
            print(data)
        else:
            # 如果缓存文件不存在，从 Yahoo Finance 下载数据
            data = yf.download(symbol, start=start_date, end=end_date)
            # 保存数据到本地缓存文件
            data.to_csv(cache_filename)
