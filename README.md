# Panoanda
Panoanda is a Pandas framework for OANDA API V1. 

## Installation

1. You can use this framework only if you have a "legacy" OANDA account (live or demo). (V20 not included)

2. You need to create a new enviroment with 3 enviroment variables :
   - "ACCOUNT" -> Your legacy OANDA account
   - "TOKEN" -> Your API token
   - "ENV" -> "practice" or "live"
   
   If you use [Anaconda](https://www.anaconda.com/distribution/ ) you can follow these steps : [Managing environments](https://conda.io/docs/user-guide/tasks/manage-environments.html)

3. Activate your enviroment and use the following command in your terminal :

    ```
    $ pip install git+https://github.com/dariocorral/panoanda.git   --process-dependency-links
    ````

    It will install all required packages.

## Usage and Examples

Panoanda includes these classes ready to use with Pandas dataframe:
 
 - Candles (Historic Candles)
 - Tickers (Info all instruments available)
 - Indicators (Some basic trading indicators)
 - Spreads (OANDA historic spreads)
 - Units (Position size calculation)
 - Financing (Financing charges calculation)

 ### Candles

 ```Python
 from panoanda.candles import Candles

 #You must create an instance
 candles = Candles()

#Dataframe 50 periods,  daily timeframe, without Sunday candle and a list:
df =  candles.dataframe(50, 'D', False, *['GBP_USD', 'USD_JPY'])
print (df)

"""Output:
           ticker	 open	  high	   low	    close	 volume	complete
2017-07-11	GBP_USD	 1.28739  1.29278  1.28309  1.2849	 45653	True
2017-07-12	GBP_USD	 1.284965 1.29082  1.28116	1.29021  61411	True
2017-07-13	GBP_USD	 1.2902	  1.29647  1.29013	1.29570	 38507	True
...
"""
 ```

 ### Tickers

 ```Python
 import pandas as pd
 from panoanda.tickers import Tickers

 #Instance
 tickers = Tickers()

 #Set a dataframe with OANDA instruments like index
 df = pd.DataFrame(index = ['EUR_USD', 'GBP_JPY', 'USD_CNH', 'AUD_USD'], data = [100, 100, 100, 100], columns = ['base'])

 #This method add a new column with tick Value for all instruments of the dataframe index

 df['tickValue'] = tickers.tick_value(df.index)

"""
Output:
        	base    tickValue
 EUR_USD	100     0.0001
 GBP_JPY	100	    0.01
 USD_CNH	100	    0.0001
 AUD_USD	100	    0.0001
"""
```
















