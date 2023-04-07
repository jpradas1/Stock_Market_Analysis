import streamlit as st
import altair as alt

import pandas as pd

import statsmodels.api as sm

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

def Stock(filtered_stock, G_Return, stock, start_date, end_date):
    # Row Top
    st.markdown('### KPIs for {} from {} to {}'.format(stock, start_date.year, end_date.year))
    col1, col2, col3 = st.columns(3)
    global_return = filtered_stock['Returns'].values[-1]
    previous_return = 1- filtered_stock['Returns'].values[-2]/filtered_stock['Returns'].values[-1]
    col1.metric("Actual Returns", "{:.2f}%".format(global_return), "{:.2f}%".format(previous_return))

    roi = (filtered_stock['Close'].values[-1] - filtered_stock['Open'].values[0]) / filtered_stock['Open'].values[0] * 100
    col2.metric("Return on Investment (ROI)", "{:.2f}%".format(roi), "")

    y = filtered_stock['Returns'].values
    X = sm.add_constant(G_Return['Global'])
    model = sm.OLS(y, X)
    results = model.fit()
    beta = results.params['Global']
    per = (beta - 1) * 100
    col3.metric("Volatility (Beta)", "{:.2f}".format(beta), "{:.0f}%".format(per))

    # Row Middle

    # st.markdown('### MACD')
    # fs = filtered_stock.reset_index()[['Date','MACD','Signal']]
    # plots = []
    # for y_col in fs.columns[1:]:
    #     plot = alt.Chart(fs).mark_line().encode(
    #         x='Date',
    #         y=y_col
    #     )
    #     plots.append(plot)

    # # Combine the line plots using the layer method
    # combined_plot = alt.layer(*plots)

    # # Display the plot in Streamlit
    # st.altair_chart(combined_plot)

    st.markdown('### MACD')
    # Melt the selected columns into long format
    filtered_stock = filtered_stock.reset_index()
    # filtered_stock['level'] = np.zeros(filtered_stock.shape[0])
    # columns = [x for x in filtered_stock[['Date', 'MACD', 'level']].columns]
    # melted_result = pd.melt(filtered_stock[columns], var_name='Date', value_name='MACD')

    line = alt.Chart(filtered_stock).mark_line().encode(
        x=alt.X('Date:N', title='Date'),
        y=alt.Y('MACD:Q', title="MACD")#, scale=alt.Scale(zero=False))
    )#.properties(width=300)

    st.altair_chart(line, use_container_width=True)