# Panoanda
Panoanda is a Pandas framework for OANDA API V1. 

## Installation

1. You can use this framework only if you have a "legacy" OANDA account (live or demo). (V20 not included)

2. You need to create a new environment with 3 environment variables :
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
 - Account (account info: NAV, balance, margin...)

 ### Candles

 ```Python
 from panoanda.candles import Candles

 #You must create an instance
 candles = Candles()

#Dataframe 50 periods,  daily timeframe, without Sunday candle and a list:
df =  candles.dataframe(50, 'D', False, *['GBP_USD', 'USD_JPY'])
print (df)

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

```
### Indicators

```Python

from panoanda.indicators import Indicators

 #Instance
 indicators = Indicators()

 #A bollinger bands dataframe (sma, std bands) according index last dataframe (df)
 df1 = indicators.boll_bands(100, 'H4', 'close', 2, *df.index)

 #Adding a column with an exponential moving average
 df1['ema'] = indicators.ema(50, 'H4', 'close', *df1.index)

 ```
### Spreads

```Python
from panoanda.spreads import Spreads

#Instance
spreads = Spreads()

#Call a dataframe with average spreads (min, avg, max) from last year
tickers = ['GBP_USD', 'USD_CAD', 'USD_JPY']
spreadsDf = spreads.dataframe('Y', *tickers)
print(spreadsDf)
```

### Units

```Python

import pandas as pd
from panoanda.units import Units

#Instance
units = Units()

#Call a dataframe with pips and amounts to trade
tickers = ['GBP_USD', 'USD_CAD', 'USD_JPY']
pips = [100, 55, 39 ]
amounts = [120, 245, 520] #account currency amounts

#Dataframe
df = pd.DataFrame(data = [tickers, pips, amounts] )
df = df.transpose()
df.columns = ('ticker', 'pips', 'amount')
df.set_index('ticker', inplace = True)

#New units column calculated according dataframe index / columns 
df['units'] = units.dataframe(*(df.index, df['pips'], df['amount']))
print(df)
```

### Financing

```Python

from panoanda.financing import Financing

#Instance
financing = Financing()

#List to use (index or columns dataframe are valid inputs too):
positions = ['long', 'short', 'long']
tickers = ['USD_CHF', 'EUR_USD', 'AUD_USD']
units = [120000, 250000, 40000] #You can use Units for this

#Interest charges for 120 hours holding position, 2 round decimals
df = financing.interest_dataframe(120, 2, *(positions, tickers, units))
print(df)

```

### Account

```Python

from panoanda.account import Account

#Instance
account = Account()

#NAV (Net asset value)
nav = account.nav
print (nav)

```

Explore help documentation to know additional functions

















