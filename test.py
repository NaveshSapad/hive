#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import shelve 
import json
from datetime import datetime as dt
import time
import altair as alt
from PIL import Image




st_hive_username=st.sidebar.empty()
st_select_token=st.sidebar.empty()
st_select_symbol=st.sidebar.empty()

st_image=st.sidebar.empty()

df=pd.read_csv(r'C:\Users\Abhishek Ravindra\Anaconda3\Hive Posting\Old\test.csv')
df=df.drop('Unnamed: 0',axis=1)


sym_list=list(set(df['symbol']))

all_list=['All']
for i in sym_list:
    all_list.append(i)

hive_user=st_hive_username.text_input('Enter your Hive username','taskmaster4450')
token=st_select_token.selectbox('Select the token you wish to see dividends for',['BRO','INDEX'])
sym= st_select_symbol.selectbox('Select SYMBOL',all_list)


if st_select_token:
    if(token=='BRO'):
        st_image.image('bro.png',use_column_width=True)
    else:
        st_image.image('tweet.png',use_column_width=True)

df_user_details=df[df['to']==hive_user]
df_user_details['quantity']=pd.to_numeric(df_user_details['quantity'])


st.title('@'+hive_user+' payouts - '+token)

if sym!='All':
    st.markdown('<hr>',unsafe_allow_html=True)
    df_sym=df_user_details[df_user_details['symbol']==sym]
    sum_sym=df_sym['quantity'].sum()

    if st.checkbox('Show table: Last 10 days '+sym+' payout'):
        st.table(df_sym.tail(10))

    st.write('<div class="comments"><center>Total '+sym+' from Jan 1 to Feb 1 : '+str(sum_sym)+' '+sym+'</center></div>',unsafe_allow_html=True)
    c = alt.Chart(df_sym).mark_line(point=True).encode(x='date', y='quantity',color='symbol',tooltip=['quantity']).interactive()
    st.write(c)
    
else:
    for sym in sym_list:
        df_sym=df_user_details[df_user_details['symbol']==sym]
        sum_sym=df_sym['quantity'].sum()

        if st.checkbox('Show table: Last 10 days '+sym+' payout'):
            st.table(df_sym.tail(10))

        st.write('<div class="comments"><center>Total '+sym+' from Jan 1 to Feb 1 : '+str(sum_sym)+' '+sym+'</center></div>',unsafe_allow_html=True)
        c = alt.Chart(df_sym).mark_line(point=True).encode(x='date', y='quantity',color='symbol',tooltip=['quantity']).interactive()
        st.write(c)
        
        

    

