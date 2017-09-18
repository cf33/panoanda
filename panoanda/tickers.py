#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 18:32:01 2017

@author: dariocorral
"""

import os
import oandapy
import pandas as pd


class Tickers(object):
    """
    Basic info about tickers available for OANDA trading
    """
    #oanda_api private attribute
    _oanda_api = oandapy.API(environment = os.environ['ENV'], 
                             access_token = os.environ['TOKEN'])
    
    @property    
    def dataframe(self):
        """
        Tickers Dataframe with basic info:
        
        :param : no params
        
        :return : dataFrame object
            
            * Pip value
            * DisplayName
            * Max Trade Units
            * Base
            * Quote
            * Pip Decimals
        """
        #Call dict OANDA API and transform to DataFrame
        df = self._oanda_api.get_instruments(OANDA_CONFIG['account'])
        df = df.get('instruments')
        df = pd.DataFrame.from_dict(df)
        base = df['instrument'].str.split('_', expand = True)
        df = df.join(base)
        df.set_index ('instrument',inplace = True)
        
        #Rename columns
        df.columns = (u'displayName', u'maxTradeUnits', u'pip', u'base',
                      u'quote')
        
        #Change tick Value to float
        df['pip'] = df['pip'].astype(float)
                
        return df

    def tick_value(self,ticker):
        """
        Minimum tick value
        
        :param: ticker
        :type : string, list or tuple
        
        :return: float or dataframe
        
        """
        return self.dataframe.loc[ticker]['pip']
    
    def display_name(self,ticker):
        """
        ticker Display Name
        
        :param: ticker 
        :type : string, list or tuple
        
        :return : string or datrame
        
        """
        return self.dataframe.loc[ticker]['displayName']

    def max_trade_units(self,ticker):
        """
        Max Trade Units allowed
        
        :param: ticker
        :type : string, list or tuple
        
        :return : integer or dataframe
        
        """
        return self.dataframe.loc[ticker]['maxTradeUnits']

    def base(self,ticker):
        """
        ticker base part
        
        :param: ticker
        :type : string, list or tuple
        
        :return : string or dataframe
        
        """
        return self.dataframe.loc[ticker]['base']

    def quote(self,ticker):
        """
        ticker quote part
        
        :param: ticker
        :type : string, list or tuple
        
        :return : string or dataframe
        
        """
        return self.dataframe.loc[ticker]['quote']
    
    def pip_decimals(self,ticker):
        """
        ticker decimals (for rounding quotes)
        
        :param: ticker
        :type : string
        
        :return : int
        
        """
        inverse =   1 / self.tick_value(ticker)
        
        return str(inverse).count('0')


  
