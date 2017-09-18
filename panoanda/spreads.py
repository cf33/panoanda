#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 10:30:16 2017

@author: dariocorral
"""

import pandas as pd
from tickers import Tickers

class Spreads(object):
    """
    Historical spread from OANDA Forex Labs
                
        * spread min
        * spread avg
        * spread max
    
    """
    
    def __init__ (self):
    
        self.__tickers = Tickers()
            
        
    def dataframe(self, timeframe,  *ticker):
        """
        Update Spreads Dataframe 

        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :paramm timeframe: OANDA timeframes:
                  “H1” - 1 hour
                  “H12” - 12 hours
                  “D” - 1 Day
                  “W” - 1 Week
                  “M” - 1 Month
                  "M3" - 3 Months
                  "M6" - 6 Months
                  "Y" - 1 Year
        :type: string
        
        :return : dataFrame object
            
        """
        
        #Spreads dataframe from dict
        df = pd.DataFrame()
        
        #Periods options
        periods = {'H1':3600, 'H12': 43200, 'D': 86400, 'W': 604800 ,
                     'M': 2592000, 'M3': 7776000, 'M6': 15552000, 'Y': 31536000}
        
        assert timeframe in ['H1', 'H12', 'D', 'W', 'M', 'M3', 'M6', 'Y'],(
                "Timeframe is not a valid value")
        
        for instr in ticker:
            
            spread_dict = (self.__tickers._oanda_api.get_historical_spreads
                                    (instrument = instr, 
                                     period = periods[timeframe]))
            spread_all = pd.DataFrame()
            
            for kind in [ 'min','avg','max']:
            
                spread = pd.DataFrame.from_dict(spread_dict [kind])
                spread = pd.DataFrame.rolling(spread, window = len(spread) ,
                                                      center = False ).mean() 
                spread['ticker'] = instr
                spread.set_index('ticker', inplace = True)
                spread.columns = [0, kind]
                spread = spread.tail(1)
                spread = spread.round(1)
                spread = spread[kind]
            
                spread_all = spread_all.append(spread)
            
            #Transpose dataframe when it is fulfilled
            spread_all = spread_all.transpose()
            
            #Build final dataframe with all tickers
            df = df.append(spread_all)
                                
        return df
    
