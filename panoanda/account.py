"""
Created on Sun Sep 17 08:13:19 2017

@author: dariocorral
"""

import os
import pandas as pd
from tickers import Tickers

class Account(object):
    """
    Class Account Info
    """
    def __init__ (self):
        
        self.__tickers = Tickers()
    
    
    @property
    def info_dataframe(self):
        """
        Dataframe Account Info
        
        no params
        
        return: dataframe object
        """
        
        df = self.__tickers._oanda_api.get_account(os.environ['ACCOUNT'])
        df = pd.DataFrame.from_dict(df, orient='index')
        df.reset_index(inplace = True)
        df.columns = ('index', 'info')
        df.set_index('index', inplace = True)
        
        return df
    
    @property
    def nav (self, round_decimals = 2):
        """
        Actual NAV (Net asset value)
        
        param: round decimals
        type: int
        
        return: float
        """
        
        df = self.info_dataframe
        
        nav = round(float(df.loc['balance'].values + 
                          df.loc['unrealizedPl'].values), round_decimals)
        
        return nav
    
    @property
    def currency(self):
        """
        Currency account
        
        no params
        
        return: str
        """
        
        df = self.info_dataframe
        
        return df.loc['accountCurrency'][0]
    
    @property
    def balance(self):
        """
        Balance 
        
        no params
        
        return: float
        """
        df = self.info_dataframe
        
        return df.loc['balance'][0]
    
    @property
    def name(self):
        """
        Name
        
        no params
        
        return: str
        """
        df = self.info_dataframe
        
        return df.loc['accountName'][0]
    
    @property
    def profit_loss(self):
        """
        Realized profits / loss
        
        no params
        
        return: float
        
        """
        df = self.info_dataframe
        
        return df.loc['realizedPl'][0]
    
    @property
    def open_trades(self):
        """
        Open Trades
        
        no params
        
        return: int
        """
        df = self.info_dataframe
        
        return df.loc['openTrades'][0]
    
    @property
    def open_orders(self):
        """
        Open Orders
        
        no params
        
        return: int
        """
        df = self.info_dataframe
        
        return df.loc['openOrders'][0]
        
    
    @property
    def margin_used(self):
        """
        Margin Used
        
        no params
        
        return: float
        """
        df = self.info_dataframe
        
        return df.loc['marginUsed'][0]
    
    @property
    def margin_available(self):
        """
        Margin Available
        
        no params
        
        return: float
        """
        df = self.info_dataframe
        
        return df.loc['marginAvail'][0]
    
    