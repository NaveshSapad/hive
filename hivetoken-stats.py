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
import matplotlib.pyplot as plt

def load_csv(token):
    if(token=='BRO'): # Use else when you add more tokens.
        df=pd.read_csv('bro_payouts.csv')
    elif(token=='INDEX'):
        df=pd.read_csv('index_payouts.csv')

    
    
    sym_list=list(set(df['symbol'])) # Take unique symbols 
    all_list=['All']
    for i in sym_list:
        all_list.append(i) # For Token selection in sidebar

    return df,all_list,sym_list

def load_image(token):
    if(token=='BRO'):
        image = Image.open('bro.png') # Get Bro image
    elif(token=='INDEX'):
        image = Image.open('index.png') # Get INDEX image
    return image

def load_user_details(df,hive_user):

    df_user_details=df[df['to']==hive_user] # This loads only specific user details 
    df_user_details['quantity']=pd.to_numeric(df_user_details['quantity']) # Converting to float.

    if df_user_details.empty:
        return df_user_details,0
    else:
        return df_user_details,1

def get_chart(df_user_details,token,sym_list,sym):

    if(token):
        if sym!='All':  # Then a particular symbol is selected in the selectbox .
            st.markdown('<hr>',unsafe_allow_html=True)

            
            df_sym=df_user_details[df_user_details['symbol']==sym] # Retreive that particular symbol details . 
            sum_sym=df_sym['quantity'].sum() # Add it .

            if st.checkbox('Show table: Last 10 days '+sym+' payout'):
                st.table(df_sym.tail(10))

            st.write('<div class="card"><div class="card-header"><center>Total '+sym+' from Jan 1 to Feb 1 : '+str(sum_sym)+' '+sym+'</center>',unsafe_allow_html=True)
            
            if sum_sym>0:
                c = alt.Chart(df_sym).mark_line(point=True).encode(x='date', y='quantity',color='symbol',tooltip=['quantity']).properties(width=750,height=500) 
                st.write(c)
            
        
        else: # Selected ALL
        
            st.markdown('<hr>',unsafe_allow_html=True)
            for sym in sym_list:
                df_sym=df_user_details[df_user_details['symbol']==sym]
                sum_sym=df_sym['quantity'].sum()

                if st.checkbox('Show table: Last 10 days '+sym+' payout'):
                    st.table(df_sym.tail(10))

                st.write('<div class="card"><div class="card-header"><center>Total '+sym+' from Jan 1 to Feb 1 : '+str(sum_sym)+' '+sym+'</center></div>',unsafe_allow_html=True)
                if sum_sym>0:
                    c = alt.Chart(df_sym).mark_line(point=True).encode(x='date', y='quantity',color='symbol',tooltip=['quantity']).properties(width=750,height=500)                
                    st.write(c)



    

if __name__ == '__main__':
    
    st.markdown('''
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    ''',unsafe_allow_html=True)

    st_hive_username=st.sidebar.empty() # Username - Empty
    st_select_token=st.sidebar.empty() # Token selection - Empty
    st_select_symbol=st.sidebar.empty() # Symbol - Empty
    st_image=st.sidebar.empty() # Image - Empty
    
    # All the above in sidebar .
    

    hive_user=st_hive_username.text_input('Enter your Hive username','amr008')
    hive_user=hive_user.lower()
    token=st_select_token.selectbox('Select the token you wish to see dividends for',['BRO','INDEX'])
    
    if token:
        df,all_list,sym_list = load_csv(token)
        
        image=load_image(token)
        st_image.image(image,use_column_width=True)

    if hive_user:
        df_user_details,n=load_user_details(df,hive_user)


    sym = st_select_symbol.selectbox('Select SYMBOL',all_list)

    if sym:
        if n==1:
            st.title('@'+hive_user+' payouts - '+token)
            st.markdown('''
            <h5>Get your {} token here - <a href='https://hive-engine.com/?p=market&t={}'>H-E Market</a></h5>
            '''.format(token,token),unsafe_allow_html=True)

            get_chart(df_user_details,token,sym_list,sym)
        else:
            st.title('@'+hive_user+' has no payouts from '+token+' to display')
            st.markdown('''
            <h5>Buy your first {} token here - <a href='https://hive-engine.com/?p=market&t={}'>H-E Market</a></h5>
            '''.format(token,token),unsafe_allow_html=True)
        
        
    
    




















