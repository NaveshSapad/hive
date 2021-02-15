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
from datetime import datetime, timedelta
    


def load_csv(token):
    st_progress.progress(12)
    if(token=='BRO'): # Use else when you add more tokens.
        df=pd.read_csv('bro_payouts.csv')
    elif(token=='INDEX'):
        df=pd.read_csv('index_payouts.csv')
    elif(token=='DHEDGE'):
        df=pd.read_csv('dhedge_payouts.csv')
    elif(token=='EDS'):
        df=pd.read_csv('EDS_payouts.csv')

    st_progress.progress(20)
    sym_list=list(set(df['symbol'])) # Take unique symbols
    all_list=[]
    if token!='EDS':
        all_list=['All']
    for i in sym_list:
        all_list.append(i) # For Token selection in sidebar

    st_progress.progress(30)
    st_proc.write("Got all the data")
    return df,all_list,sym_list


def load_image(token):
    if(token=='BRO'):
        image = Image.open('bro.png') # Get Bro image
    elif(token=='INDEX'):
        image = Image.open('index.png')# Get INDEX image
    elif(token=='DHEDGE'):
        image = Image.open('dhedge.png') # Get DHEDGE image
    elif(token=='EDS'):
        image = Image.open('EDS.png') # Get EDS image
    
    return image

def load_user_details(df,hive_user,token):
    st_progress.progress(55)
    st_proc.write("Filtering your data")

    sum_hive_yesterday=0 # To calculate yesterday's hive payout

    df_user_details=df[df['to']==hive_user] # This loads only specific user details 
    df_user_details['quantity']=pd.to_numeric(df_user_details['quantity']) # Converting to float.

    date_count=len(set(df_user_details['date']))

    
    if not df_user_details.empty:
        st_proc.write("Fetching payouts for {} account".format(hive_user))
        df_last_date=df_user_details[df_user_details['date']==max(df_user_details['date'])]
        
        df_last_date.reset_index(inplace=True)
        st_progress.progress(65)

        if token!='EDS':
            for i in range(0,len(df_last_date)):
                sum_hive_yesterday += get_token_price(df_last_date['symbol'][i])*df_last_date['quantity'][i]
        else:
            sum_hive_yesterday = df_last_date['quantity'][0]

        if st.checkbox("Click here to see most recent date payout "):
            st.table(df_last_date)
    st_progress.progress(85)
    
            



    if df_user_details.empty:
        return df_user_details,0,date_count,sum_hive_yesterday
    else:
        return df_user_details,1,date_count,sum_hive_yesterday

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
                st.table(df_sym.head(10))

            market=Market() # Market instance
            list_metrics=market.get_metrics() # Returns all the tokens in HE with details
            for i in list_metrics:
                if(i['symbol']==sym): # Selecting only the symbol we want
                    total=(float(i['lastPrice'])* sum_sym) # Taking last price and multiplying with total token earned which is = sum_sym

            if sym=='HIVE':
                total=sum_sym

            total_hive=total
                                
            st.write('<div class="card"><div class="card-header"><center>Total '+sym+' from Jan 1 to  Feb 14: '+ '%.6f' % sum_sym+' '+sym+' , In HIVE = '+'%.6f' % total +'.</center>',unsafe_allow_html=True)
            
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
                    st.table(df_sym.head(10))


                market=Market() # Market instance
                list_metrics=market.get_metrics() # Returns all the tokens in HE with details
                for i in list_metrics:
                    if(i['symbol']==sym): # Selecting only the symbol we want
                        total=(float(i['lastPrice'])* sum_sym) # Taking last price and multiplying with total token earned which is = sum_sym

                total_hive=total_hive+total
                
                if sym=='HIVE':
                    total=sum_sym
            
                st.write('<div class="card"><div class="card-header"><center>Total '+sym+' from Jan 1 to Feb 14 : '+'%.6f' % sum_sym+' '+sym+' , In HIVE = '+'%.6f' %total+'.</center>',unsafe_allow_html=True)
            
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

    st.markdown('''
    <iframe data-aa="1567652" src="//ad.a-ads.com/1567652?size=728x90" scrolling="no" style="width:728px; height:90px; border:0px; padding:0; overflow:hidden" allowtransparency="true"></iframe>
    
    ''',unsafe_allow_html=True)

    

    st_hive_username=st.sidebar.empty() # Username - Empty
    st_select_token=st.sidebar.empty() # Token selection - Empty
    st_select_symbol=st.sidebar.empty() # Symbol - Empty
    st_image=st.sidebar.empty() # Image - Empty
    st_proc=st.sidebar.empty() 
    st_progress=st.sidebar.empty()
 

    hive_user=st_hive_username.text_input('Enter your Hive username','amr008')
    hive_user=hive_user.lower()
    token=st_select_token.selectbox('Select the token you wish to see dividends for',['BRO','INDEX','DHEDGE','EDS'])
    
    if token:
        start=dt.now()
        st_progress.progress(10)
        df,all_list,sym_list = load_csv(token)

        
        image=load_image(token)
        st_image.image(image,use_column_width=True)

    if hive_user:
        df_user_details,n,date_count,sum_hive=load_user_details(df,hive_user,token)
        st_proc.write("Data Loaded")
        st_progress.progress(100)


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
            

            if token!='EDS':
                APR = (((sum_hive) * 365) / (float(balance) * current_token_price )*100)
            else:
                APR = (((sum_hive) * 52) / (float(balance) * current_token_price )*100)
                APR1=  (((sum_hive) * 52) / (float(balance) * 1 )*100)
            
            if token!='EDS':
                st_total_hive.markdown('<hr><hr><h3>Total Hive from {} token from Jan 1 to Feb 14 is: {} HIVE<br> <hr> Per day average(Hive) for the above period from {} token= {} HIVE.<br><hr>Yesterdays payout ( in Hive ) ={} Hive <br><hr> APR (based on most recent payout + Recent price of {}):{} % </h3>'.format(sym,'%.5f' % total_hive,sym,'%.4f' %per_day_average,"%.5f"%sum_hive,token,"%.2f"%APR),unsafe_allow_html=True)
            else:
                st_total_hive.markdown('<hr><hr><h3>Total Hive from EDS to your account is: {} HIVE<br><br><hr>Most recent payout ( in Hive ) ={} Hive <br><hr> APR (based on most recent payout + Recent price of {}):{}% <br><hr> Since most of the users bought EDS at 1 HIVE - APR ( based on EDS price as 1 HIVE ) = {}% </h3>'.format('%.5f' % total_hive,sum_hive,token,"%.2f"%APR,"%.2f"%APR1),unsafe_allow_html=True)

            
            
        else:
            st.title('@'+hive_user+' has no payouts from '+token+' to display')
            st.markdown('''
            <h5>Buy your first {} token here - <a href='https://hive-engine.com/?p=market&t={}'>H-E Market</a></h5>
            '''.format(token,token),unsafe_allow_html=True)
