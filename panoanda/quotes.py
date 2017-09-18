"""
Created on Sun Sep 17 07:24:48 2017

@author: dariocorral
"""


import pandas as pd
from datetime import timedelta
from hourOffset import Hour
from tickers import Tickers
from account import Account

class Quotes(object):
    
    """
    OANDA Ticker Quotes ready to use with Pandas 
    """
    def __init__(self):
        
        self.__tickers = Tickers()
        self.__hour = Hour()   
        self.__account = Account()
            
    def dataframe(self,field,*ticker):
    
        """
        Actual OANDA quotes
        
        :param field: 'bid', 'ask', 'mid', 'spread', 'all'
        :type: str
        
        :param ticker: required instruments format OANDA API
        :type: str, tuple or list
        
        :return: dataFrame object
        
        """
        
        quotesTotal = pd.DataFrame()
            
        for instr in ticker: 
                quotes = self.__tickers._oanda_api.get_prices(instruments = 
                              instr)
                quotes = quotes.get('prices')
                quotes = pd.DataFrame(quotes)
                quotes['mid'] = round((quotes['bid'] + quotes['ask']) / 2,
                      self.__tickers.pip_decimals(instr))
                                
                quotes.set_index('instrument', inplace = True)
                quotes = quotes[['bid','ask','mid','time']]
                quotes['time'] = pd.to_datetime(quotes['time'])
                quotes['time'] = quotes['time'] + timedelta(hours = 
                                 self.__hour.offset_local_GMT)
                quotes['spread'] = round(((quotes['ask'] - quotes['bid']) 
                                / self.__tickers.tick_value(instr)), 1)
                quotesTotal = quotesTotal.append(quotes)
        
        if field == 'all':
        
            return quotesTotal
        
        else:
            
            return quotesTotal[field]
    
    def ticker_bid (self,ticker) :
        """
        Actual Oanda ticker bid quote
        
        :param ticker: required instrument format OANDA API
        :type: str
        
        :return: float
        
        """
        return float(self.dataframe('bid',ticker).values)
    
    def ticker_ask (self,ticker) :
        """
        Actual Oanda ticker ask quote
        
        :param ticker: required instrument format OANDA API
        :type: str
        
        :return: float
        
        """
        return float(self.dataframe('ask',ticker).values)
    
    def ticker_mid (self,ticker) :
        """
        Actual Oanda ticker mid quote
        
        :param ticker: required instrument format OANDA API
        :type: str
        
        :return: float
        
        """

        return float(self.dataframe('mid',ticker).values)
    
    def ticker_spread (self,ticker) :
        """
        Actual Oanda ticker spread
        
        :param ticker: required instrument format OANDA API
        :type: str
        
        :return: float
        
        """

        return float(self.dataframe('spread',ticker).values)

    def __currency_account_pricing_notUSD(self,pair):
        """
        Return mid quote pairs not included in tickers.dataframe
        included exotic pairs quoted in account base currency NOT USD
        
        :param pair: instrument or mix of them
        :type: str
        
        :return: float
        """
        base = pair.split('_') [0]
        quote = pair.split('_') [1]
        
        #Check if the account currency is in base or quote vs USD -> Bool 
        curr = self.__account.currency
        
        curr_base = ((curr + '_' + 'USD') in 
                        self.__tickers.dataframe.index)
        
        inversed_pair = quote + '_' + base
        
        #Possibilities and output
        if base == quote:
            
            return 1
        
        elif pair in self.__tickers.dataframe.index:
            
            return self.ticker_mid(pair)
        
        elif inversed_pair in self.__tickers.dataframe.index:
            
            return (1 / self.ticker_mid(inversed_pair))
        
        elif curr_base == True and (('USD'+'_'+base) in 
                                        self.__tickers.dataframe.index):

            return ((1 / self.ticker_mid('USD'+'_'+base)) * 
                    (1 / self.ticker_mid(curr + '_' + 'USD')))
        
        elif curr_base == True and ((base+'_'+'USD') in 
                                        self.__tickers.dataframe.index):
            
            return (self.ticker_mid(base+'_'+'USD') *  
                    (1 / self.ticker_mid(curr + '_' + 'USD')))
            
        
        elif curr_base == False and (('USD'+'_'+base) in 
                                        self.__tickers.dataframe.index):
            
            return ((1 / self.ticker_mid('USD'+'_'+base)) * 
                    (self.ticker_mid('USD' + '_' + 
                    self.__account.currency )))
            
        elif curr_base == False and ((base+'_'+'USD') in 
                                        self.__tickers.dataframe.index):
            
            return (self.ticker_mid(base+'_'+'USD') *  
                    (self.ticker_mid('USD' + '_' + 
                    self.__account.currency )))
        
        #A pair not quoted in USD
        elif (curr_base == False or True) and ((base+'_'+'USD') not in 
                                        self.__tickers.dataframe.index):
            
            #Not quoted in USD, searching quoted ticker
            reference = self.__tickers.dataframe.loc[
                    self.__tickers.dataframe['base'] == base].index.values[0] 
            
            quote_ref = reference.split('_') [1]
            
            if (quote_ref+'_'+quote) in self.__tickers.dataframe.index:
            
                return (self.ticker_mid(reference) * 
                        (self.ticker_mid(quote_ref+'_'+quote)))
            
            else:
                
                return (self.ticker_mid(reference) * 
                        (1 / self.ticker_mid(quote+'_'+quote_ref)))
            
    def __currency_account_pricing_USD(self,pair):
        """
        Return mid quote pairs not included in tickers.dataframe
        included exotic pairs quoted in account base currency (USD acc currency)
        
        :param pair: instrument or mix of them
        :type: str
        
        :return: float
        """
        base = pair.split('_') [0]
        quote = pair.split('_') [1]
                        
        inversed_pair = quote + '_' + base
        
        #Possibilities and output
        if base == quote:
            
            return 1
        
        elif pair in self.__tickers.dataframe.index:
            
            return self.ticker_mid(pair)
        
        elif inversed_pair in self.__tickers.dataframe.index:
            
            return (1 / self.ticker_mid(inversed_pair))
        
        #A pair not quoted in USD
        else:    
            
            #Ticker dataframe
            df = self.__tickers.dataframe
            
            #Not quoted in USD, searching quoted ticker
            reference = df.loc[
                    df['base'] == base].index.values[0] 
            
            quote_ref = reference.split('_') [1]
            
            if (quote_ref+'_'+quote) in self.__tickers.dataframe.index:
            
                return (self.ticker_mid(reference) * 
                        (self.ticker_mid(quote_ref+'_'+quote)))
            
            else:
                
                return (self.ticker_mid(reference) * 
                        (1 / self.ticker_mid(quote+'_'+quote_ref)))
    
    def currency_account_pricing(self, *pair):
        """
        Return mid quote pairs not included in tickers.dataframe
        included exotic pairs quoted in account base currency
        
        :param pair: instrument or mix of them
        :type: str, list, tuple or index
        
        :return: dataframe object
        """
        curr = self.__account.currency
                
        df_total = pd.DataFrame()
        
        if curr != 'USD':
        
            for instr in pair:
                
                df = pd.DataFrame({'ticker': instr, 
                            'quote': [self.__currency_account_pricing_notUSD(instr)]}) 
                df.set_index('ticker',inplace = True)
                    
                df_total = df_total.append(df)
                
            return df_total
    
        else:
            
            for instr in pair:
                
                df = pd.DataFrame({'ticker': instr, 
                            'quote': [self.__currency_account_pricing_USD(instr)]}) 
                df.set_index('ticker',inplace = True)
                    
                df_total = df_total.append(df)
                
            return df_total
            
            