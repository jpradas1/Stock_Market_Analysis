# Stock Market Analysis

This repository provides an analitics analysis of Stock Market, mainly the companies beloging to S&P500. The principal analysis is developed throughout the jupyter notebooks [Analysis I](https://github.com/jpradas1/Stock_Market_Analysis/blob/main/Analysis_I.ipynb) and [Analysis II](https://github.com/jpradas1/Stock_Market_Analysis/blob/main/Analysis_II.ipynb). In these notebook it takes place a set of invesment advicent to a fictional client who wants to know whether to invest in the Energy sector, in which sub-industries and companies to get significative earnings.

Thus use has been made of parameter such as Volatility, Return, Risk, Moving Average Convergence Divergence, Return on investment, etc, in order to analyse the Market and take a final decision for our cliente.

Furthermore, the dashword display through [stramlit](https://streamlit.io/) with the aim to analyze the Market graphically has multiple option to anaylize the previous parameter by sector, sub-industry and stock, and group data by year, month-year and week-year and hence reaching information to short, middle and long-term.


## How to Display de Dashboard
First let's download the necesary libraries
```
python -m venv venv
source venv/bin/activate
pip intall -r requirement.txt
```

To display the dashboard there are two important python scipts to take into account. First, we need download Stock Market data from yfinance, this can be done by running the [get_dataset's](https://github.com/jpradas1/Stock_Market_Analysis/blob/main/get_dataset.py) function *create_csv()*, i.e.,

```
python3 get_dataset.py True
```
Finally to display the interactive dashboard, just run:
```
streamlit run dashboard-app.py
```
