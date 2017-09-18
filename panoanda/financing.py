"""
Created on Sun Sep 17 10:07:17 2017

@author: dariocorral
"""

import os
import pandas as pd
from tickers import Tickers
from quotes import Quotes
from account import Account


class Financing(object):
    """
    Financing Charges Class
    """
    
    def __init__(self):
        self.__tickers = Tickers()
        self.__quotes = Quotes()
        self.__account = Account()
    
    def __update_raw_dataframe(self):
        """
        Secondary call method in order to update dataframe
        
        :no params: 
            
        """
        
        data = (self.__tickers._oanda_api.get_instruments
                (os.environ['ACCOUNT'], fields= 'interestRate' ))
        
        #Creating an empty DataFrame
        df = pd.DataFrame() 
        
        # Iterating over the instruments list
        for item in data['instruments']:  
            df = pd.concat([df, pd.DataFrame.from_dict(item)
            .join(pd.DataFrame.from_dict(item['interestRate'], 
                                         orient='index'))])
        
        # Performing some cleaning to get back a proper interestRate column   
        df = df.drop('interestRate', axis=1).reset_index().rename(
                        columns={'index':'interestRate'})
        df = df.drop('instrument',1)
        df.drop_duplicates(inplace=True)
        df.index = df ["interestRate"]
        df = df.drop('interestRate',1)
        df.columns =[['bid','ask']]
        
        return  df 
    
    @property
    def dataframe(self):
        """
        Returns ticker interest rate according long/short positions
        
        :No params:
            
        return: dataframe object
        
        """
        #Update raw interest dataframe
        df = self.__update_raw_dataframe()
        
        df_bid = df['bid'] * 100
        df_ask = df['ask'] * 100
        
        dfTotal = pd.DataFrame()
        
        for instr in list(self.__tickers.dataframe.index): 
        
            ticker_split = instr.split('_')
                                        
            long_interest = round((df_ask[ticker_split[0]] -  
                                df_bid[ticker_split[1]]),2)
                        
            short_interest = round(((-df_bid[ticker_split[0]]) +  
                                df_ask[ticker_split[1]]),2)
            
            df = {instr : [long_interest, short_interest]}
            df = pd.DataFrame.from_dict(df, 'index')
            
            dfTotal= dfTotal.append(df)
            
        dfTotal.columns = ('long', 'short')
                
        return dfTotal
    
    def calculate(self,position, ticker,units, hours=120, round_decimals=1):
        """
        Returns financing charges for a position:
        
        :param : position :'long' or 'short'
        :type: str
        
        :param : ticker : 'EUR_USD', 'USD_JPY'
        :type: str
        
        :param : units : total units of the position 
        :type: int
        
        :param: hours : hours keeping the position
        :type: int
        
        :return: financing charges 
        :type: float
        
        --Formula--
        
        For a long position:
            
        Financing Charges on Base = units * ({BASE} Interest Rate %) * 
                                    (Time in years) * ({BASE}/Primary Currency)
        
        Financing Charges on Quote = (converted units) * ({QUOTE} Interest Rate %)
                                    * (Time in years) * ({QUOTE}/Primary Currency)
        
        Total Financing = Financing Charges on Base - Financing Charges on Quote
        
        For a short position:
            
        Financing Charges on Quote = (converted units) * ({QUOTE} Interest Rate %) 
        * (Time in years) * ({QUOTE}/Primary Currency)
        
        Financing Charges on Base = units * ({BASE} Interest Rate %) * 
        (Time in years) * ({BASE}/Primary Currency)
        
        Total Interest = Financing Charges on Quote - Financing Charges on Base    
        """
        
        assert position in ['long', 'short'], ("Position value must be 'long'" 
                                               "or 'short'")
        
        
        int_rate = self.__update_raw_dataframe()
        
        base = ticker.split('_') [0]
        quote = ticker.split('_') [1]
        time = float((hours /24.0) / 365.0)
        curr = self.__account.currency

        if curr == 'USD':

            base_curr = self.__quotes.__currency_account_pricing_USD(base + '_' + curr)        
            quote_curr = self.__quotes.__currency_account_pricing_USD(quote + '_' + curr)
            base_quote = self.__quotes.__currency_account_pricing_USD(base+ '_' + quote)
        
        else:

            base_curr = self.__quotes.__currency_account_pricing_notUSD(base + '_' + curr)        
            quote_curr = self.__quotes.__currency_account_pricing_notUSD(quote + '_' + curr)
            base_quote = self.__quotes.__currency_account_pricing_notUSD(base+ '_' + quote)


        if position == 'long':
                 
            base_int_rate = (units * int_rate.loc[base]['ask'] * time * 
                                 base_curr)
            
            quote_int_rate = ((units * (base_quote)) * 
                                    int_rate.loc[quote]['bid'] * time * 
                                    quote_curr  )
        
            total_int = base_int_rate - quote_int_rate
        
            return round(total_int, round_decimals)
            
        elif position == 'short':
            
            quote_int_rate = ((units * (base_quote)) * 
                                  int_rate.loc[quote]['ask'] * time *
                                  quote_curr)
            
            base_int_rate = (units * int_rate.loc[base]['bid'] * time *
                             base_curr)
                    
            total_int =  quote_int_rate - base_int_rate
            
            return round (total_int, round_decimals)
        
        
    def interest_dataframe(self,hours,round_decimals, *args):
        """
        Returns weekly interest of keeping a position along a week
        in dataframe format
        
        Example:
            
            financing = Financing()
            financing.weekly_interest_dataframe(hours,2, *(position, tickers, units))
            
            position, tickers and units -> list, tuple or dataframe index
        
        """
        
        df_total = pd.DataFrame()
        
        for position, instr, units in zip(*args):
            
            financing = self.calculate(hours = hours, round_decimals=round_decimals, 
                                       position = position, units = units,
                                       ticker = instr)
            
            df_output = pd.DataFrame({'ticker': instr, 
                                      'Fin': [financing]})            
            df_output.set_index('ticker',inplace = True)
            
            df_total = df_total.append(df_output)
        
        return df_total
          