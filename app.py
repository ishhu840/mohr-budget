from typing import ValuesView
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import random
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title = "PSDP - 2023-24", page_icon=":bar_chart:",layout="wide")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#st.title('Uber pickups in NYC')
df =  pd.read_excel(
    io="psdp.xlsx",
    engine='openpyxl',
    sheet_name='data',
    skiprows= 0,
    usecols='A:L',
    nrows=50000,
)
#print(df)
#st.dataframe(df)

st.sidebar.header("Please Filter Here :")
PName = st.sidebar.multiselect(
    "Select the Project :",
    options=df["projectname"].unique(),
    default=df["projectname"].unique()

)

HName = st.sidebar.multiselect(
    "Select the Expenditure Head of Account:",
    options=df["head"].unique(),
    default=df["head"].unique()

)


df_selection = df.query(
    "projectname == @PName & head == @HName"
)



st.title(" :bar_chart: PSDP (FY 2023-24) - Budget Execution ( Dashboard) ")
#st.markdown("#")

total_budget = df_selection ['Original Budget'].sum() / 1000000
released_budget = df_selection ['Released Budget'].sum() / 1000000
total_expenditure = df_selection ['Expenditure'].sum() / 1000000
#total_expenditure = df_selection ['Expenditure'].sum() 

left_column , middle_column , right_column = st.columns(3)

with left_column:
    st.header("Total Budget :" f" {total_budget}", "M")
    #st.subheader(f" {total_cases}")  

with middle_column:
   # st.header("Total Victim :"f"{total_vic}")
    st.header("Released Budget :"f"{released_budget}")

  #  st.subheader(f"{total_vic}")
   # st.subheader(" :mens: Male Victim : "f"{total_maleV}")
   # st.subheader(" :womens: Female Victim : "f"{total_femaleV}")
  

with right_column :
    st.header("Expenditure :"f"{total_expenditure}")
    #st.subheader(f"{total_fir}") 
    #st.subheader("Arrested :"f"{total_arrested}")

st.markdown("---")


left_column , right_column = st.columns(2)

with left_column:
    labels = 'Total Budget','Release'
    sizes = [ total_budget - released_budget , released_budget]
    explode = (0,0.1)
  #  title="Total Budget & Release in %"
    fig1 , ax1  = plt.subplots() 
    ax1.pie(sizes, explode=explode, labels=labels , autopct='%1.01f%%',
            shadow=False, startangle= 60 )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Total Budget &  Release %")
    st.pyplot(fig1 )

with right_column:
    labels = 'Released Budget','Expenditure'
    expenditure_percentage = (total_expenditure / released_budget) * 100
    sizes = [100 - expenditure_percentage, expenditure_percentage]  # Calculate the remaining budget percentage
    explode = (0,0.1)
    fig1 , ax1  = plt.subplots() 
    ax1.pie(sizes, explode=explode, labels=labels , autopct='%1.01f%%',
            shadow=False, startangle= 60 )
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Released Budget / Expenditure %")
    st.pyplot(fig1 )

st.markdown("##")
st.markdown("---")
st.markdown("##")


option = st.selectbox(
     'Select the Project ',
     (PName))

st.markdown("##")
#st.write('You selected:', option)


df_selection = df.query("projectname == @option")
#print(df_selection.head()) 
df = df_selection.groupby('head')['Expenditure'].sum().reset_index()

# Plot Bars
plt.figure(figsize=(16, 10), dpi=80)
plt.bar(df['head'], df['Expenditure'], color='skyblue', width=0.5)

for i, val in enumerate(df['Expenditure'].values):
    plt.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight': 500, 'size': 12})
# Decoration
plt.gca().set_xticklabels(df['head'], rotation=60, horizontalalignment='right')
plt.title("Expenditure " + str(option) + " (Head-Wise)", fontsize=22 , pad=40)
#plt.ylim(0, df['Expenditure'].max() + 50)
plt.ylim(0, df['Expenditure'].max() + 500) 
st.pyplot(plt)

st.markdown("##")
st.markdown("---")
st.markdown("##")
