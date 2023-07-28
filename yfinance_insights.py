# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 19:59:36 2023

@author:
         udayl: https://github.com/Udayl56

    Yfinance Ticker Stock Insights using streamlit app 
    
"""
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly_express as px
from stocknews import StockNews

#config
st.set_page_config(page_title="Yfinance Ticker Stock Insights",page_icon="📈",layout="wide",initial_sidebar_state="expanded",)

# this is header
t1,t2=st.columns((3,2))
t1.title("Yfinance Ticker Stock Insights")
t2.markdown("**For Detailed Documentation | GitHub:** https://github.com/Udayl56 ")
  
#------------------------------------------------------------------------------

##########################
#      sidebar
##########################
             
df=pd.read_csv('yfinance-ticker-list.csv')  # Ticker list of symbols downloading
choice = st.sidebar.selectbox("Select Ticker",df)
symbol = yf.Ticker(choice)

if "key" not in st.session_state:
   
    st.session_state.key=0
    st.session_state.key=choice
    
    
START = date(2023,1,1)
TODAY = date.today()

if "st" not in st.session_state:
    st.session_state.st=0

if "et" not in st.session_state:
    st.session_state.et=0
    
start_date = st.sidebar.date_input("Start date",START)
end_date = st.sidebar.date_input("End date",TODAY,)

st.session_state.st=start_date
st.session_state.et=end_date

tickerDf=symbol.history(period="1d",start=st.session_state.st,end=st.session_state.et)
tickerDf.reset_index(inplace=True)

with st.sidebar:
    
    # Ticker information
    regularMarketOpen=symbol.info['regularMarketOpen']
    currentPrice=symbol.info["currentPrice"]
    currancy=symbol.info["currency"]
    exchange=symbol.info["exchange"]
    sector=symbol.info["sector"]
    industry=symbol.info["industry"]
    st.write("***Regular Market Open :***",str(regularMarketOpen))
    style_metric_cards()
    st.metric("***Current Price :***",currentPrice)
    st.write("***Currancy:***", currancy)
    st.write("***Exchange:***",exchange)
    st.write("***Sector:***",sector)
    st.write("***Industry:***",industry)
#------------------------------------------------------------------------------    

longname=symbol.info["longName"] #display longname of ticker
st.subheader(longname)

#tabs    
tab1, tab2, tab3,tab4,tab5,tab6 = st.tabs(["Sumaary", "Chart","Custom Area Chart","Comparision Chart","Fundamental Data","News"]) 

##########################
#   Summary Tab
##########################    
    
with tab1:
    
    c11,c12,c13,c14=st.columns(4) # In Row 1
    
    c11.metric("PreviousClose",symbol.info["previousClose"])
    c12.metric("Open",symbol.info["open"])
    c13.metric("DayLow",symbol.info["dayLow"])
    c14.metric("DayHigh",symbol.info["dayHigh"])
    
    c21,c22,c23,c24= st.columns(4) # In Row 2
    
    c21.metric("52 Week Low",symbol.info["fiftyTwoWeekLow"])
    c22.metric("52 Week High",symbol.info["fiftyTwoWeekHigh"])
    c23.metric("52 Week Average",symbol.info["fiftyDayAverage"])
    cc24=symbol.info["52WeekChange"]
    c24.metric("52 Week Change",cc24,cc24)
    
    c31,c32,c33,c34=st.columns(4) # In Row 3
    
    c31.metric("Volume",symbol.info["volume"])
    c32.metric("Regular Market Volume",symbol.info["regularMarketVolume"])
    c33.metric("Average Volume",symbol.info["averageVolume"])
    c34.metric("Average Volume 10days",symbol.info["averageVolume10days"])

#------------------------------------------------------------------------------ 
   
k=pd.DataFrame(tickerDf) 
k.drop(['Volume','Dividends','Stock Splits'],axis=1,inplace=True)  
  
##########################
#    Chart tab 2
##########################    
    
with tab2, st.spinner('Loading...'):
    
    time.sleep(3)
    st.markdown(""" :green[Double Click on Variable Option and See Costum Chart]""")
    
    fig1=px.line(k,x='Date',y=k.columns,hover_data={"Date": "|%B %d, %Y"}, width=1000, height=420)
    fig1.update_xaxes(rangeslider_visible=True,dtick="M1",tickformat="%b\n%Y",ticklabelmode="period",showgrid=True)
    st.plotly_chart(fig1)
#------------------------------------------------------------------------------
##########################
#   Custom Area Chart tab 3
##########################        
    
with tab3,st.spinner('Loading ...'):
    
    time.sleep(3)
    
    p1,p2,p3,p4=st.columns(4)
    
    fig3 = px.area(k,x=k.Date,y='Open')
    fig3.update_xaxes(rangeslider_visible=True)
    
    p1.plotly_chart(fig3)
    
    fig4 = px.area(k,x=k.Date,y='Close')
    fig4.update_xaxes(rangeslider_visible=True)
    
    p2.plotly_chart(fig4, use_container_width=True)
    
    fig5 = px.area(k,x=k.Date,y='High')
    fig5.update_xaxes(rangeslider_visible=True)
    
    p3.plotly_chart(fig5, use_container_width=True)
    
    fig6 = px.area(k,x=k.Date,y='Low')
    fig6.update_xaxes(rangeslider_visible=True)
    
    p4.plotly_chart(fig6, use_container_width=True)    
#------------------------------------------------------------------------------
##########################
#   Comparison Chart tab 4
##########################

with tab4,st.spinner('Loading ...'):
   
    
    #choicekey=st.session_state.key
    ms=st.selectbox("Adj Closed Stock Price in % change", df)
    
    time.sleep(3)
    
    symbol1=yf.Ticker(ms)
    st.write('Company:',symbol1.info["longName"])
    mdf=yf.download(ms,start=start_date,end=end_date)
    
    mdf.drop(['Open','High','Low','Close','Volume'],axis=1,inplace=True)
    mdf['% change ' + str(ms)]=mdf['Adj Close']/mdf['Adj Close'].shift(1)-1
    
    mdf1=yf.download(choice,start=start_date,end=end_date)
    
    mdf1.reset_index(inplace=True)
    mdf1.drop(['Open','Close','Volume','High','Low'],axis=1,inplace=True)
    mdf1['% change '+str(choice)]=mdf1['Adj Close']/mdf1['Adj Close'].shift(1)-1
    
    kk=mdf1.drop(['Adj Close'],axis=1)
    md2=pd.merge(left=kk,right=mdf['% change ' +str(ms)],how='right', on='Date')
    
    
    fig6=px.bar( md2,x='Date',y= md2.columns,width=1000, height=400)
    st.plotly_chart(fig6)
#------------------------------------------------------------------------------
##########################
#  Fundamental Data tab 5
##########################    
 
with tab5,st.spinner('Loading ...'):
    time.sleep(3)
    def datasetselect():
        
        cho1=["Balance Sheet","Cash Flow","MutualFund Holders","Earning Day"]
        
        sel=st.selectbox("Dataset",cho1)
        
        if "Balance Sheet"==sel:
            st.write(symbol.balance_sheet)
        elif "Cash Flow"==sel:
            st.write(symbol.cashflow)
        elif "MutualFund Holders"==sel:
             st.write(symbol.mutualfund_holders)   
        elif "Earning Day"==sel:
              st.write(symbol.earnings_dates)
              return None
    datasetselect()    
#------------------------------------------------------------------------------
##########################
#  News tab 6
########################## 

with tab6,st.spinner('Loading ...'):
    
    st.markdown(":red[last 5 day's News ]")
    time.sleep(3)
    sn= StockNews(choice,save_news=False)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f'News {i+1}')
        st.caption(df_news['published'][i])
        title=df_news['title'][i]
        st.write(f'***{title}***')
        st.write(df_news['summary'][i])
        

                      # Thanks for review
#------------------------------------------------------------------------------





