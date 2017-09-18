#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 09:27:31 2017

@author: dariocorral
"""

import pandas as pd
from datetime import timedelta
from tickers import Tickers
from hourOffset import Hour


class Candles(object):
    """
    OANDA Historical Rates ready to use with Pandas
    """
    
    def __init__(self):
        
        self.__hour = Hour()
        self.__tickers = Tickers()

    
    def dataframe(self,periods, granularity,sundayCandle, *ticker):
        """
        OANDA Historical Rates
        
        :param periods: number of periods
        :type: int
        
        :paramm granularity: OANDA timeframes:
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
        :type: string
        
        :param sundayCandle: True -> Sunday Candles included
                             False -> No Sunday Candles 
        :type : bool
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
                    
        """        
        #Define empty dataframe
        df = pd.DataFrame()
        
        for instr in ticker:
            
            histRates =  self.__tickers._oanda_api.get_history(count =
                              int(periods * 1.2), instrument= instr,
                              candleFormat = 'midpoint',granularity= granularity,
                              dailyAlignment= (self.__hour.hour_offset_calculate(
                                                  6 , 
                                               self.__hour.offset_NY_GMT)), 
                              weeklyAlignment='Monday')
                        
            #From dict to dataframe 
            histRates = histRates.get('candles')
            histRates = pd.DataFrame.from_dict(histRates)
            histRates['ticker'] = instr
            histRates['time'] = pd.to_datetime(histRates['time'])
            
            #Apply GMT_hours_offset to local time
            histRates['time'] += timedelta(hours = 
                             self.__hour.offset_local_GMT)
            histRates.set_index ('time', inplace = True)
            
            #Sunday candle filter
            if sundayCandle == False:
                
                histRates['Weekday'] = histRates.index.weekday
                histRates = histRates.loc[histRates['Weekday'] != 6]
                histRates = histRates.tail(periods)
            
            else: 
                
                histRates = histRates.tail(periods)
            
            #Daily and weekly granularity in date format without hours
            if granularity == 'D' or granularity == 'W':
                
                histRates.index = histRates.index.date 
            
            #Columns definition
            histRates= histRates[['ticker','openMid','highMid','lowMid',
                                  'closeMid','volume','complete']]
            
            histRates.columns = ('ticker','open','high','low','close','volume',
                    'complete')
            
            df = df.append(histRates)
       
        return df 
    