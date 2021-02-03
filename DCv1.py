# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
class DCv1(IStrategy):
    #
    ticker_interval = '1h'
    startup_candle_count = 120
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False
    process_only_new_candles = False
    # ROI
    minimal_roi = {
        "0" : 1.0,
     "5760" : 0.0,
     "7200" : -1.0
    }
    # Stoploss
    stoploss = -0.25
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_only_offset_is_reached = True
    trailing_stop_positive_offset = 0.1
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['dc_up'] = dataframe['high'].rolling(48).max()
        dataframe['dc_low'] = dataframe['low'].rolling(48).min()
        dataframe['dc_mid'] = (dataframe['high'] + dataframe['low'])/2.
        dataframe['trend'] = ta.EMA(dataframe, timeperiod=240)
        return dataframe
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            (dataframe['high'] > dataframe['dc_up'].shift()) &
            (dataframe['close'] > dataframe['trend'])
            ),
        'buy'] = 1
        return dataframe
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            (dataframe['low'] < dataframe['dc_low'].shift())
            ),
        'sell'] = 1
        return dataframe
