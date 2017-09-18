#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 16:36:46 2017

@author: dariocorral
"""
import pandas as pd
from tickers import Tickers
from quotes import Quotes
from candles import Candles


class Indicators(object):
    """
    Trading Indicators
    """
    
    def __init__ (self):
        
        self.__tickers = Tickers()
        self.__candles = Candles()
        self.__quotes = Quotes()
    
    def sma(self,periods, granularity, applyTo, *ticker):
        """
        Simple Moving Average
                
        :param periods: number of Simple Moving Average periods
        :type: int
        
        :param granularity: OANDA Timeframes:
                  “S5” - 5 seconds
                  “S10” - 10 seconds
                  “S15” - 15 seconds
                  “S30” - 30 seconds
                  “M1” - 1 minute
                  “M2” - 2 minutes
                  “M3” - 3 minutes
                  “M4” - 4 minutes
                  “M5” - 5 minutes
                  “M10” - 10 minutes
                  “M15” - 15 minutes
                  “M30” - 30 minutes
                  “H1” - 1 hour
                  “H2” - 2 hours
                  “H3” - 3 hours
                  “H4” - 4 hours
                  “H6” - 6 hours
                  “H8” - 8 hours
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
        :type: str
                    
        :param applyTo: close, open, high, low or volume
        :type: str
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        
        """
        if applyTo in ['close','open', 'high', 'low', 'volume']:
            
            ibsDf = pd.DataFrame()
            
            for instr in ticker: 
                
                df = self.__candles.dataframe(periods, 
                                                  granularity,False, instr)
                df = df[applyTo]
                df = df.rolling(periods, center = False).mean()
                df = {instr : (round(float(df.tail(1).values), 
                                      self.__tickers.pip_decimals(instr)))}
                df = pd.DataFrame.from_dict(df, 'index')
                ibsDf = ibsDf.append(df)
            
            ibsDf.reset_index(inplace = True)
            ibsDf.columns = ('ticker', 'sma')
            ibsDf.set_index('ticker', inplace = True)
            
            return ibsDf

        else:
            
            raise ValueError ("Please enter 'close','open','high','low'" 
                              "or 'volume'")

    def ema(self,periods, granularity, applyTo, *ticker):
        """
        Exponential Moving Average
                
        :param periods: number of Simple Moving Average periods
        :type: int
        
        :param granularity: OANDA Timeframes:
                  “S5” - 5 seconds
                  “S10” - 10 seconds
                  “S15” - 15 seconds
                  “S30” - 30 seconds
                  “M1” - 1 minute
                  “M2” - 2 minutes
                  “M3” - 3 minutes
                  “M4” - 4 minutes
                  “M5” - 5 minutes
                  “M10” - 10 minutes
                  “M15” - 15 minutes
                  “M30” - 30 minutes
                  “H1” - 1 hour
                  “H2” - 2 hours
                  “H3” - 3 hours
                  “H4” - 4 hours
                  “H6” - 6 hours
                  “H8” - 8 hours
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
        :type: str
                    
        :param applyTo: close, open, high, low or volume
        :type: str
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        
        """
        if applyTo in ['close','open', 'high', 'low', 'volume']:
            
            ibsDf = pd.DataFrame()
            
            for instr in ticker: 
                df = self.__candles.dataframe(periods, 
                              granularity,False, instr)
                df = df[applyTo]
                df = df.ewm( span = periods, min_periods = periods - 1).mean()
                df = {instr : (round(float(df.tail(1).values), 
                                      self.__tickers.pip_decimals(instr)))}
                df = pd.DataFrame.from_dict(df, 'index')
                ibsDf = ibsDf.append(df)
            
            ibsDf.reset_index(inplace = True)
            ibsDf.columns = ('ticker', 'ema')
            ibsDf.set_index('ticker', inplace = True)
            
            return ibsDf

        else:
            
            raise ValueError ( "Please enter 'close','open','high','low'" 
                              "or 'volume'")

    def ibs(self, periods, granularity, *ticker):
        """
        Internal Bar Strength
        
        Formula: 
            IBS =  (Close – Low) / (High – Low) * 100
                
        :param periods: number of IBS periods
        :type: int
        
        :param granularity: OANDA Timeframes:
                  “S5” - 5 seconds
                  “S10” - 10 seconds
                  “S15” - 15 seconds
                  “S30” - 30 seconds
                  “M1” - 1 minute
                  “M2” - 2 minutes
                  “M3” - 3 minutes
                  “M4” - 4 minutes
                  “M5” - 5 minutes
                  “M10” - 10 minutes
                  “M15” - 15 minutes
                  “M30” - 30 minutes
                  “H1” - 1 hour
                  “H2” - 2 hours
                  “H3” - 3 hours
                  “H4” - 4 hours
                  “H6” - 6 hours
                  “H8” - 8 hours
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
        :type: str
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        """
        ibsDf = pd.DataFrame()
        
        for instr in ticker: 
        
            df = self.__candles.dataframe(periods , 
                                                  granularity,False,instr)
            df_max = df['high'].max()
            df_min = df['low'].min()
            df_close = df ['close'].tail(1).values
            ibs = ((df_close - df_min ) / (df_max - df_min )) * 100
            ibs = int(ibs)
            ibsDict = {instr: ibs}
            df = pd.DataFrame.from_dict(ibsDict, 'index')
            ibsDf = ibsDf.append(df)

        ibsDf.reset_index(inplace = True)
        ibsDf.columns = ('ticker', 'ibs')
        ibsDf.set_index('ticker', inplace = True)
        
        return ibsDf
    
    def boll_bands(self, periods, granularity, applyTo, stdDev, *ticker):
        """
        Bollinger Bands with Simple Moving Average
        
        :param periods: number of Simple Moving Average periods
        :type: int
        
        :param granularity: OANDA Timeframes:
                  “S5” - 5 seconds
                  “S10” - 10 seconds
                  “S15” - 15 seconds
                  “S30” - 30 seconds
                  “M1” - 1 minute
                  “M2” - 2 minutes
                  “M3” - 3 minutes
                  “M4” - 4 minutes
                  “M5” - 5 minutes
                  “M10” - 10 minutes
                  “M15” - 15 minutes
                  “M30” - 30 minutes
                  “H1” - 1 hour
                  “H2” - 2 hours
                  “H3” - 3 hours
                  “H4” - 4 hours
                  “H6” - 6 hours
                  “H8” - 8 hours
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
        :type: str
                    
        :param applyTo: close, open, high, low or volume
        :type: str
        
        :stdDev : is a number of standard deviations to include in the envelope.
        :type: float
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        """
        bbDf = pd.DataFrame()
        
        for instr in ticker: 
        
            df = self.__candles.dataframe(int(periods * 2) , 
                                                  granularity,False,instr)
            df['sma'] = (df[applyTo].rolling(periods, center = False).mean()).round(5)
            df['std']= df[applyTo].rolling(periods, center = False).std()
            df['upBand'] = (df['sma'] + (df['std'] * stdDev)).round(5)
            df['dnBand'] = (df['sma'] - (df['std'] * stdDev)).round(5)
            df.reset_index(inplace = True)
            df.set_index('ticker', inplace = True)
            df = df[['dnBand','sma','upBand']].tail(1)
            bbDf = bbDf.append(df)
        
        return bbDf
   
    def atr(self,periods, granularity, kind, *ticker):
        """
        Average True Range
        
        :param periods: number of Exponential Moving Average periods
        :type: int
        
        :param granularity: OANDA Timeframes:
                  “S5” - 5 seconds
                  “S10” - 10 seconds
                  “S15” - 15 seconds
                  “S30” - 30 seconds
                  “M1” - 1 minute
                  “M2” - 2 minutes
                  “M3” - 3 minutes
                  “M4” - 4 minutes
                  “M5” - 5 minutes
                  “M10” - 10 minutes
                  “M15” - 15 minutes
                  “M30” - 30 minutes
                  “H1” - 1 hour
                  “H2” - 2 hours
                  “H3” - 3 hours
                  “H4” - 4 hours
                  “H6” - 6 hours
                  “H8” - 8 hours
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
        :type: str
        
        :param kind: 'raw' or 'pips' format
        :type: str
                            
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        """
        atrDf = pd.DataFrame()
        
        for instr in ticker: 
            
            df = self.__candles.dataframe(periods * 2 , 
                                   granularity, False, instr)
            df1 = df['close'].shift(1)
            df1.name = ('close1')
            df = pd.concat([df,df1], axis = 1)               
            df['range1'] = df['high'] - df['low']
            df['range2'] = abs(df['close1'] - df ['high'])
            df['range3'] = abs ( df['close1'] - df['low']) 
            df['atr'] = df[['range1', 'range2','range3']].max(axis=1)
            df.reset_index(inplace = True)
            df.set_index('ticker', inplace = True)
            df['atr'] = df['atr'].ewm( span = periods, 
                         min_periods = periods - 1).mean()
            df = df['atr']         
            df = df.tail(1).round(self.__tickers.pip_decimals(instr))
            atrDict = {instr: float(df.values)}
            df = pd.DataFrame.from_dict(atrDict, 'index')
            atrDf = atrDf.append(df)
        
        atrDf.reset_index(inplace = True)
        atrDf.columns = ('ticker', 'atr')
        atrDf.set_index('ticker', inplace = True)
        
        if kind == 'raw':
        
            return atrDf
        
        elif kind == 'pips':
            
            atrDf = (atrDf['atr'] / 
                             self.__tickers.dataframe.loc[atrDf.index]['pip'])
            return atrDf
        
        else: 
            
            raise ValueError( "Please type 'raw' or 'pips'")

    def atr_channels(self, periods, granularity, multiple, *ticker):
        """
        ATR Channels
        
        :param periods: number of Simple Moving Average periods
        :type: int
        
        :param granularity: OANDA Timeframes:
                  “S5” - 5 seconds
                  “S10” - 10 seconds
                  “S15” - 15 seconds
                  “S30” - 30 seconds
                  “M1” - 1 minute
                  “M2” - 2 minutes
                  “M3” - 3 minutes
                  “M4” - 4 minutes
                  “M5” - 5 minutes
                  “M10” - 10 minutes
                  “M15” - 15 minutes
                  “M30” - 30 minutes
                  “H1” - 1 hour
                  “H2” - 2 hours
                  “H3” - 3 hours
                  “H4” - 4 hours
                  “H6” - 6 hours
                  “H8” - 8 hours
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
        :type: str
        
        :multiple : is a number of ATRs to include in the envelope.
        :type: float
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        """
        atrChDf = pd.DataFrame()
        
        for instr in ticker: 
            
            df = self.__candles.dataframe(int(periods * 2) , 
                                    granularity,  False,instr)
            df['typicalPrice'] = ((df['high'] + df['low'] + df['close']) 
                                / 3).round(self.__tickers.pip_decimals(instr))
            
            df['range'] = df['high'] - df['low']
            
            df['smaTP'] = (df['typicalPrice'].rolling(periods, 
                                              center = False).mean())
            df['smaRange'] = (df['range'].rolling(periods, 
                                              center = False).mean())
            
            df['upChan'] = df['smaTP'] + (df['smaRange'] * multiple)
            df['dnChan'] = df['smaTP'] - (df['smaRange'] * multiple)
            
            df.reset_index(inplace = True)
            df.set_index('ticker', inplace = True)
            df = df[['dnChan','smaTP','upChan']].tail(1)
            atrChDf = atrChDf.append(df)
        
        return atrChDf

     
    def max_min_quotes(self, periods, granularity, kind, *ticker):
        """
        Returns max or min of a defined period of time
        
        :param :periods
        :type: int
        
        :param :granularity:
              “D” - 1 Day
              “W” - 1 Week
              “M” - 1 Month
        :type: str
        
        :param: ticker
        :type: str, list, tuple or index
        
        :param: kind - 'max' or 'min'
        :type: str
        
        :return: dataframe object
        
        """
        if granularity not in ['D', 'W', 'M']:
            raise ValueError("Granularity must be 'D', 'W' or 'M' values" )
        
        if kind not in ['max', 'min']:
            raise ValueError("Kind must be 'max' or 'min' values" )
        
        df_total = pd.DataFrame()
                
        for instr in ticker:
        
            df = self.__candles.dataframe((periods * 2), 
                                              granularity,False, instr)
            df = df.loc[df['complete'] == True].copy()
            
            choice_dict = {'max':'high', 'min': 'low'}
            
            if kind == 'min':
            
                df['max_min'] = df[choice_dict[kind]].rolling(periods , 
                                  center = False).min()
            
            elif kind == 'max' :
               
                df['max_min'] = df[choice_dict[kind]].rolling(periods , 
                                  center = False).max()
                    
            max_min = float(df['max_min'].tail(1)) 
            
            df_output = pd.DataFrame({'ticker': instr, 
                                      'max_min': [max_min]})            
            df_output.set_index('ticker',inplace = True)
            
            df_total = df_total.append(df_output)
        
        return df_total