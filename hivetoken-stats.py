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
from hiveengine.wallet import Wallet
from hiveengine.market import Market


@st.cache
def load_csv(token):
    if(token=='BRO'): # Use else when you add more tokens.
        df=pd.read_csv('bro_payouts.csv')
    elif(token=='INDEX'):
        df=pd.read_csv('index_payouts.csv')
    elif(token=='DHEDGE'):
        df=pd.read_csv('dhedge_payouts.csv')

    
    
    sym_list=list(set(df['symbol'])) # Take unique symbols 
    all_list=['All']
    for i in sym_list:
        all_list.append(i) # For Token selection in sidebar

    return df,all_list,sym_list

@st.cache
def load_image(token):
    if(token=='BRO'):
        image = Image.open('bro.png') # Get Bro image
    elif(token=='INDEX'):
        image = Image.open('index.png')# Get INDEX image
    elif(token=='DHEDGE'):
        image = Image.open('dhedge.png') # Get DHEDGE image
    return image

def load_user_details(df,hive_user):

    df_user_details=df[df['to']==hive_user] # This loads only specific user details 
    df_user_details['quantity']=pd.to_numeric(df_user_details['quantity']) # Converting to float.

    date_count=len(set(df_user_details['date']))

    if df_user_details.empty:
        return df_user_details,0,date_count
    else:
        return df_user_details,1,date_count

def get_balance(hive_user,token):
    wallet=Wallet(hive_user)

    list_balances=wallet.get_balances()
    for i in range(0,len(list_balances)):
        if(list_balances[i]['symbol']==token):
            return(list_balances[i]['balance'])
    return(0)

def get_chart(df_user_details,token,sym_list,sym):
    total_hive=0
    my_bar.progress(20)
    total=0

    if(token):
        if sym!='All':  # Then a particular symbol is selected in the selectbox .
            st.markdown('<hr>',unsafe_allow_html=True)

            
            df_sym=df_user_details[df_user_details['symbol']==sym] # Retreive that particular symbol details . 
            sum_sym=df_sym['quantity'].sum() # Add it .

            if st.checkbox('Show table: Last 10 days '+sym+' payout'):
                st.table(df_sym.tail(10))

            market=Market() # Market instance
            list_metrics=market.get_metrics() # Returns all the tokens in HE with details
            for i in list_metrics:
                if(i['symbol']==sym): # Selecting only the symbol we want
                    total=(float(i['lastPrice'])* sum_sym) # Taking last price and multiplying with total token earned which is = sum_sym

            if sym=='HIVE':
                total=sum_sym

            total_hive=total
                                
            st.write('<div class="card"><div class="card-header"><center>Total '+sym+' from Jan 1 to Feb 4 : '+ '%.6f' % sum_sym+' '+sym+' , In HIVE = '+'%.6f' % total +'.</center>',unsafe_allow_html=True)
            
            if sum_sym>0:
                c = alt.Chart(df_sym).mark_line(point=True).encode(x='date', y='quantity',color='symbol',tooltip=['quantity']).properties(width=750,height=500) 
                st.write(c)

            my_bar.progress(50)

            return total_hive

        
        
        else: # Selected ALL
            n=0
            for sym in sym_list:
                n=n+1
                my_bar.progress((n/len(sym_list)))
                
                st.markdown('<hr>',unsafe_allow_html=True)
                st.header(sym)
                df_sym=df_user_details[df_user_details['symbol']==sym]
                sum_sym=df_sym['quantity'].sum()

                if st.checkbox('Show table: Last 10 days '+sym+' payout'):
                    st.table(df_sym.tail(10))


                market=Market() # Market instance
                list_metrics=market.get_metrics() # Returns all the tokens in HE with details
                for i in list_metrics:
                    if(i['symbol']==sym): # Selecting only the symbol we want
                        total=(float(i['lastPrice'])* sum_sym) # Taking last price and multiplying with total token earned which is = sum_sym

                total_hive=total_hive+total
                
                if sym=='HIVE':
                    total=sum_sym
            
                st.write('<div class="card"><div class="card-header"><center>Total '+sym+' from Jan 1 to Feb 4 : '+'%.6f' % sum_sym+' '+sym+' , In HIVE = '+'%.6f' %total+'.</center>',unsafe_allow_html=True)
            
                if sum_sym>0:
                    c = alt.Chart(df_sym).mark_line(point=True).encode(x='date', y='quantity',color='symbol',tooltip=['quantity']).properties(width=750,height=500)                
                    st.write(c)

            
            return total_hive


def get_token_price(token):
    market=Market() # Market instance
    list_metrics=market.get_metrics() # Returns all the tokens in HE with details
    for i in list_metrics:
        if(i['symbol']==token): # Selecting only the symbol we want
            return(float(i['lastPrice']))

    return(0)
    



    

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
    token=st_select_token.selectbox('Select the token you wish to see dividends for',['BRO','INDEX','DHEDGE'])
    
    if token:
        df,all_list,sym_list = load_csv(token)
        
        image=load_image(token)
        st_image.image(image,use_column_width=True)

    if hive_user:
        df_user_details,n,date_count=load_user_details(df,hive_user)


    sym = st_select_symbol.selectbox('Select SYMBOL',all_list)

    balance=get_balance(hive_user,token)

    if sym:
        if n==1:       
            st.title('@'+hive_user+' payouts: '+token)
            st.subheader('Your current balance: '+str(balance)+' '+token)
            st.markdown('''
            <h5>Buy more {} token here - <a href='https://hive-engine.com/?p=market&t={}'>H-E Market</a></h5>
            '''.format(token,token),unsafe_allow_html=True)

            st_total_hive=st.empty()

            st_display_progress=st.empty()

            my_bar = st_total_hive.progress(0)

            my_bar.progress(10)
            st_display_progress.write("Please wait while the all the payouts details loads completely to calculate final HIVE")
            

            total_hive=get_chart(df_user_details,token,sym_list,sym)

            my_bar.progress(100)
            st_display_progress.empty()
            

            per_day_average= total_hive/date_count

            current_token_price= get_token_price(token)
            
            #APR = ((per_day_average * 365) / (float(balance) * current_token_price )*100)


            st_total_hive.markdown('<hr><hr><h3><center>Total Hive from {} token from Jan 1 to Feb 4 is: {} HIVE<br> <hr> Per day average(Hive) from {} token= {} HIVE.  </center></h3>'.format(sym,'%.5f' % total_hive,sym,'%.4f' %per_day_average),unsafe_allow_html=True)
            
            
        else:
            st.title('@'+hive_user+' has no payouts from '+token+' to display')
            st.markdown('''
            <h5>Buy your first {} token here - <a href='https://hive-engine.com/?p=market&t={}'>H-E Market</a></h5>
            '''.format(token,token),unsafe_allow_html=True)
        
        
    
    




















