from pytrends.request import TrendReq
import pandas as pd
from model import User, Company, Following, StockPrice, Interest, connect_to_db, db

from flask import Flask
from server import app
import datetime


interest = TrendReq(hl='en-US', tz=360) # connect to google trends
kw_list = ["etsy"] # set keyword
interest.build_payload(kw_list, geo='US', timeframe='today 12-m', cat=0) # build pay load

# returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.
# return type : pandas dataframe
interest_df = interest.interest_over_time() 
interest_df = interest_df.iloc[:,:1] # get rid of isPartial column

def load_interests():

    for row in interest_df.iterrows():
        
        date, value = row[0], row[1] # date : datetime / interest : pandas series.
        value = value.to_dict()
        value = Interest(date=date, interest=value["etsy"])
        
        db.session.add(stock_price)
        db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_interests()

