import streamlit as st
import altair as alt

import pandas as pd

def Sectors(filtered_sector, df_returns, risk, plot_data, 
            start_date, end_date):
    
    # Row Top
    st.markdown('### General Information by Sectors from {} to {}'.format(start_date.year, end_date.year))
    col1, col2, col3 = st.columns(3)
    global_return = round(filtered_sector.sum(axis=1).iloc[-4:].pct_change()*100,2)
    previous_return = 1- global_return.iloc[-2]/global_return.iloc[-1]
    col1.metric("Global Returns", "{:.2f}%".format(global_return.iloc[-1]), "{:.2f}%".format(previous_return))

    high_sector = risk.iloc[risk['Total Return'].idxmax()].values[0]
    hs_return = round(filtered_sector[[high_sector]].iloc[-4:].pct_change()*100,2)
    hs = 1 - hs_return.iloc[-2].values[0]/hs_return.iloc[-1].values[0]
    col2.metric("Highest Return Sector", "{}".format(high_sector), "{:.2f}%".format(hs))

    low_sector = risk.iloc[risk['Total Return'].idxmin()].values[0]
    ls_return = round(filtered_sector[[low_sector]].iloc[-4:].pct_change()*100,2)
    ls = 1 - ls_return.iloc[-2].values[0]/ls_return.iloc[-1].values[0]
    col3.metric("Lowest Return Sector", "{}".format(ls_return), "{:.2f}%".format(ls))


    # Row Middle a

    st.markdown('### Adjusted Close Price (USD)')
    # st.line_chart(filtered_sector, x = 'Date', y = plot_data)
    columns = filtered_sector.columns
    chart_data = pd.DataFrame({
        k: filtered_sector[k] for k in columns
    })
    chart = st.line_chart(chart_data, x = 'Date', y = plot_data)

    # Row Middle b

    st.markdown('### Volatility')
    # Melt the selected columns into long format
    columns = [x for x in df_returns.columns]
    melted_result = pd.melt(df_returns[columns], var_name='Sector', value_name='Return')

    box = alt.Chart(melted_result).mark_boxplot().encode(
        x=alt.X('Sector:N', title=None),
        y=alt.Y('Return:Q', title=None, scale=alt.Scale(zero=False))
    ).properties(width=300)

    st.altair_chart(box, use_container_width=True)


    # Row Bottom
    c1, c2 = st.columns((7,7))
    with c1:
        st.markdown('### Risk')
        c = alt.Chart(risk).mark_circle().encode(
            x = 'Expected Return',
            y = 'Volatility',
            size = 'Total Return',
            color = 'Sector',
            tooltip = [x for x in risk.columns]
        ).configure_legend(disable=True).interactive()
        st.altair_chart(c)
    with c2:
        st.markdown('### Total Return')
        b = alt.Chart(risk).mark_bar().encode(
            x = 'Total Return',
            y = 'Sector',
            color = 'Sector'
        ).configure_legend(disable=True).interactive()
        st.altair_chart(b, use_container_width=True)

def Industry(filtered_sub, df_returns, risk, plot_data, 
            start_date, end_date):
    # Row Top
    st.markdown('### General Information by Industry from {} to {}'.format(start_date.year, end_date.year))
    col1, col2, col3 = st.columns(3)
    global_return = round(filtered_sub.sum(axis=1).iloc[-4:].pct_change()*100,2)
    previous_return = 1- global_return.iloc[-2]/global_return.iloc[-1]
    col1.metric("Global Returns", "{:.2f}%".format(global_return.iloc[-1]), "{:.2f}%".format(previous_return))

    high_sub = risk.iloc[risk['Total Return'].idxmax()].values[0]
    hs_return = round(filtered_sub[[high_sub]].iloc[-4:].pct_change()*100,2)
    hs = 1 - hs_return.iloc[-2].values[0]/hs_return.iloc[-1].values[0]
    col2.metric("Highest Return Industry", "{}".format(high_sub), "{:.2f}%".format(hs))

    low_sub = risk.iloc[risk['Total Return'].idxmin()].values[0]
    ls_return = round(filtered_sub[[low_sub]].iloc[-4:].pct_change()*100,2)
    ls = 1 - ls_return.iloc[-2].values[0]/ls_return.iloc[-1].values[0]
    col3.metric("Lowest Return Industry", "{}".format(ls_return), "{:.2f}%".format(ls))

    # Row Middle a

    st.markdown('### Adjusted Close Price (USD)')
    # st.line_chart(filtered_sector, x = 'Date', y = plot_data)
    columns = filtered_sub.columns
    chart_data = pd.DataFrame({
        k: filtered_sub[k] for k in columns
    })
    chart = st.line_chart(chart_data, x = 'Date', y = plot_data)

    # Row Middle b

    st.markdown('### Volatility')
    # Melt the selected columns into long format
    columns = [x for x in df_returns.columns]
    melted_result = pd.melt(df_returns[columns], var_name='Sector', value_name='Return')

    box = alt.Chart(melted_result).mark_boxplot().encode(
        x=alt.X('Sector:N', title=None),
        y=alt.Y('Return:Q', title=None, scale=alt.Scale(zero=False))
    ).properties(width=300)

    st.altair_chart(box, use_container_width=True)

    # Row Bottom
    c1, c2 = st.columns((7,7))
    with c1:
        st.markdown('### Risk')
        c = alt.Chart(risk).mark_circle().encode(
            x = 'Expected Return',
            y = 'Volatility',
            size = 'Total Return',
            color = 'Sector',
            tooltip = [x for x in risk.columns]
        ).configure_legend(disable=True).interactive()
        st.altair_chart(c)
    with c2:
        st.markdown('### Total Return')
        b = alt.Chart(risk).mark_bar().encode(
            x = 'Total Return',
            y = 'Sector',
            color = 'Sector'
        ).configure_legend(disable=True).interactive()
        st.altair_chart(b, use_container_width=True)