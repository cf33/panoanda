# Panoanda
Panoanda is a Pandas framework for OANDA API V1. 

## Installation

1. You can use this framework only if you have a "legacy" OANDA account (live or demo). (V20 not included)

2. You need to create a new enviroment with 3 enviroment variables :
   - "ACCOUNT" -> Your legacy OANDA account
   - "TOKEN" -> Your API token
   - "ENV" -> "Practice" or "live"
   
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

 #Candles

 ```Python
 from panoanda.candles import Candles

 #You must create an instance
 candles = Candles()

#Dataframe 50 periods,  daily timeframe, without Sunday candle and a list:
df =  candles.dataframe(50, 'D', False, *['GBP_USD', 'USD_JPY'])
print (df)
 ```

 #Tickers

 








