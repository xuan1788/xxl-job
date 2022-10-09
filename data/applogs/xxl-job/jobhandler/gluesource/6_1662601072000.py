#!/usr/bin/python
# -*- coding: UTF-8 -*-

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import sys
sys.path.append('/Users/xuan/Documents/transmatrix/')
import numpy as np

from transmatrix03.matrix.base import MatrixConfig, BaseMatrix
from transmatrix03.trader.base import StrategyConfig, BaseStrategy

# 初始化回测管理组件 matrix
mat_config = MatrixConfig(
    {
        'backtest_span': ['2021-07-01','2021-07-30']
    }
)
mat = BaseMatrix(mat_config)

#配置策略信息

#策略1
stra_info0 = {'name': 'strategy0',
              'subscribe_info':
                [
                    ['stock_cn__bar__30min','002594.SZSE,000002.SZSE'],
                ]
             }

#策略2
stra_info1 = {'name': 'strategy1',
              'subscribe_info':
                [
                    ['stock_cn__bar__30min','002594.SZSE,000002.SZSE'],
                ]
            }

config0 = StrategyConfig(stra_info0)
config1 = StrategyConfig(stra_info1)

# 策略编写 
class TestStrategy(BaseStrategy):

    # 为进行压力测试，我们让策略在多个市场随机报撤单

    choices = ['000002.SZSE','002594.SZSE']
    N = len(choices)

    def on_market_data_update(self, market):

        code = self.choices[np.random.choice(self.N)]
        data = market.data
        price = data.get(fields = 'close', codes = code)
    
        prob = np.random.randn()
        if prob > 1.5:
            self.buy(price,100,'open',code,'stock_cn__bar__30min')
        elif prob < -1.5:
            self.sell(price,100,'open',code,'stock_cn__bar__30min')

stra0 = TestStrategy(config0, mat)
stra1 = TestStrategy(config1, mat)

mat.init_markets()
mat.init_timeline()
mat.run()    