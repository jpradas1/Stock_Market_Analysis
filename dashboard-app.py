import streamlit as st
import pandas as pd

from get_dataset import Finance
from get_dataset import Returns_Risk, MACD, global_return
from pages_dashboard import Sectors, Industry, Stock

F = Finance()

# primary settings
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('Analysis on Stock Market')


# Date & DataFrame
data_sector = F.adj_close_mean_sector().reset_index()
data_sector['Date'] = pd.to_datetime(data_sector['Date']).dt.date

# left sidebar settings
page1 = "Sector"
page2 = "Sub-Industry"
page3 = "Stock"
pages = {"Sector": page1, "Sub-Industry": page2, "Stock": page3}
page_choice = st.sidebar.multiselect("Stock Market Leaf", list(pages.keys()))


#--> sidebar: Row Middle
st.sidebar.subheader('Select Sector')
sidebar_sector = st.sidebar.multiselect('Select Sector', F.get_sector())

#--> slidebar: Row Middle
min_date, max_date = data_sector['Date'].min(), data_sector['Date'].max()
start_date = st.sidebar.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

#--> select gruopby (year, month, week)
time_type = st.sidebar.radio(
    "Select how to group data by:",
    ('Year', 'Month-Year', 'Week-Year'))


# Filter the data based on the selected date range
mask = (data_sector['Date'] >= pd.to_datetime(start_date).date()) & \
        (data_sector['Date'] <= pd.to_datetime(end_date).date())

# Filtered Data & DataFrames
filtered_sector = data_sector.loc[mask]
sector_returns, sector_risk = Returns_Risk(filtered_sector.set_index('Date'), time_type)


# display
if "Sector" in page_choice:
    Sectors(filtered_sector, sector_returns, sector_risk, sidebar_sector,
            start_date, end_date)
    

## Sub-Industries
st.sidebar.subheader('Select Sub-Industry')
sidebar_industry = None
if sidebar_sector:
    sidebar_industry = st.sidebar.multiselect('Select Sub-Industry', F.get_subindustry(sector=sidebar_sector[0]))
    data_sub = F.adj_close_total_sub(sector=sidebar_sector[0]).reset_index()
    data_sub['Date'] = pd.to_datetime(data_sub['Date']).dt.date

    # Filter the data based on the selected date range
    mask = (data_sub['Date'] >= pd.to_datetime(start_date).date()) & \
            (data_sub['Date'] <= pd.to_datetime(end_date).date())
    
    filtered_sub = data_sub.loc[mask]
    sub_returns, sub_risk = Returns_Risk(filtered_sub.set_index('Date'),time_type)

    if "Sub-Industry" in page_choice:
        Industry(filtered_sub, sub_returns, sub_risk, sidebar_industry, start_date, end_date)

## Stocks
st.sidebar.subheader('Select Stock')
if sidebar_industry:
    sidebar_stock  = st.sidebar.multiselect('Select Sub-Industry', \
                        F.get_stock(sector=sidebar_sector[0], sub=sidebar_industry[0]))

    if "Stock" in page_choice:
        
        g_return = global_return(start_date).dropna()
        
        for st in sidebar_stock:
            data_stock = MACD(sector=sidebar_sector[0], sub=sidebar_industry[0], stock=st, start_date=start_date)
            Stock(data_stock, g_return, st, start_date, end_date)