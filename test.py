#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import shelve 
import json
from datetime import datetime as dt
import time

st1=st.empty()
st_input=st.empty()
df=pd.read_csv('test.csv')
df=df.drop('Unnamed: 0',axis=1)
name=st_input.text_input('Enter your Hive username')

st.write('Your selected username='+name)
df1=df[df['to']==name]

df1['quantity']=pd.to_numeric(df1['quantity'])

sym=st.text_input('Enter Symbol')

df_sym=df1[df1['symbol']==sym]
df_sym=df_sym.set_index(df_sym['date'])
sum_sym=df_sym['quantity'].sum()
if sym!='':
    st.write('Total '+sym+' from Jan 1 to Feb 1 : '+str(sum_sym)+' '+sym)
else:
    st.write('Please enter Symbol')
st.line_chart(df_sym['quantity'])



