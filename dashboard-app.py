import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

number = np.random.choice(10)

color_dict = {
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
}

lista = ["Item 1", "Item 2", "Item 3"]

items_str = "<ul>"
for item in lista:
    items_str += "<li>{}</li>".format(item)
items_str += "</ul>"

items_str2 = "<ul>"
for color, hexcode in color_dict.items():
    items_str2 += "<li><span style='background-color:{}; padding: 5px; \
            border-radius: 50%; display: inline-block; margin-right: 10px;\
            '></span>{}</li>".format(hexcode, color)
items_str2 += "</ul>"

page1 =  """
        <div style='display: flex; justify-content: space-between;'>
            <div style='background-color: #ffb3ba; padding: 20px; width: 30%;'>
                <h3>Global Return</h3>
                <p>{}</p>
            </div>
            <div style='background-color: #ffdfba; padding: 20px; width: 30%;'>
                <h3>Top Sectors</h3>
                {}
            </div>
            <div style='background-color: #bae1ff; padding: 20px; width: 30%;'>
                {}
            </div>
        </div>
        """.format(number, items_str, items_str2)
page2 = "This is page 2"
page3 = "This is page 3"

pages = {"Sector": page1, "Subindustries": page2, "Stock": page3}

# Add a multiselect widget to choose the page
page_choice = st.sidebar.multiselect("Stock Marcket Leaf", list(pages.keys()))

# Display the content for the selected page
# for choice in page_choice:
#     st.write(pages[choice])

# if "Sector" in page_choice:

row1 = st.columns([1])[0]
with row1:
    st.markdown(page1 , unsafe_allow_html=True)

row2 = st.columns([1])[0]
with row2:
    plt.figure(figsize=(15,5))
    sns.set_style("whitegrid")
    tips = sns.load_dataset("tips")
    ax = sns.violinplot(x="day", y="total_bill", hue="sex", data=tips, split=True)
    st.pyplot(ax.figure)

row31, row32, row33 = st.columns([1, 1, 1])
with row31:
    sns.set_style("whitegrid")
    iris = sns.load_dataset("iris")
    ax1 = sns.boxplot(x="species", y="sepal_length", data=iris)
    st.pyplot(ax1.figure)

with row32:
    sns.set_style("whitegrid")
    iris = sns.load_dataset("iris")
    ax2 = sns.scatterplot(x="sepal_width", y="petal_length", hue="species", data=iris)
    st.pyplot(ax2.figure)

with row33:
    sns.set_style("whitegrid")
    iris = sns.load_dataset("iris")
    ax3 = sns.violinplot(x="species", y="petal_length", data=iris)
    st.pyplot(ax3.figure)