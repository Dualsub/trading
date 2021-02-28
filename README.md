# Trading Bot
Python program that uses a simple MACD-indicator to determine when to sell and buy stocks. :chart_with_upwards_trend:

## Backtesting
Backtesting on old data is used to analyse the efficiency of the algoritm. This data is retrived through the [IEX Cloud](https://iexcloud.io/) REST-api.

***DISCLAMER:***
* The data used is not true histoical data, but still resembles real stock movements.
* Commission is not taken into account with the current model.

#### Examples of profitable results:

![plot](./figures/OPK_2021-02-15.png)
![plot](./figures/EGRNF_2021-02-15.png)
![plot](./figures/TR_2021-02-15.png)

#### Examples of less profitable results:

![plot](./figures/IRBT_2021-02-16.png)
![plot](./figures/BNGO_2021-02-15.png)
