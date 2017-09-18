#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 09:51:13 2017

@author: dariocorral
"""


import pandas as pd
from quotes import Quotes
from tickers import Tickers
from account import Account


class Units(object):
    """
    Units calculation class
    
    """
    
    def __init__(self):
        
        self.__quotes = Quotes()
        self.__tickers = Tickers()
        self.__account = Account()
        
            
    def ticker(self, ticker, pips, amount):
        """
        Returns units calculated according an currency account amount
        
        :param: ticker
        :type: str
        
        :param: pips
        :type: int
        
        :param: amount (account currency)
        :type: float
        
        :return: int
        """
        #Define variables
        quote = ticker.split('_')[1]
        
        
        
        #It is not available EUR_XXX quotes but we can get this value
        # doing (1 / XXX_EUR)
        position_risk_quote = (amount * (1 / 
                               self.__quotes._currency_account_pricing(
                              quote + '_' +  self.__account.currency)))
        
        pip_value_quote = position_risk_quote / pips
        
        units = (pip_value_quote * (1 / 
                             self.__tickers.tick_value(ticker)))
        
        return int(round(units,0))
    
    def dataframe(self, *args):
        """
        Returns units calculated dataframe format
        
        Example:
            
            units.dataframe( 300, *(tickers, pips))
            
            tickers, pips -> list, tuple or dataframe index
    
        """
        
        df_total = pd.DataFrame()
        
        for instr, pips, amount  in zip(*args):
            
            units = self.ticker(instr,pips, amount)
            
            df_output = pd.DataFrame({'ticker': instr, 
                                      'units': [units]})            
            df_output.set_index('ticker',inplace = True)
            
            df_total = df_total.append(df_output)
        
        return df_total