from pytrends.request import TrendReq
import pandas as pd
from model import User, Company, Following, StockPrice, Interest, connect_to_db, db
from forms import SelectForm, RegisterForm

from flask import Flask, render_template, redirect, request, flash, session, url_for

import datetime



interest = TrendReq(hl='en-US', tz=360) # connect to google trends
kw_list = ["Groupon"] # set keyword
interest.build_payload(kw_list, timeframe='today 12-m') # build pay load

# returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.
# return type : pandas dataframe
interest_df = interest.interest_over_time() 
interest_df = interest_df.iloc[:,:1] # get rid of isPartial column

def load_interests():

    for row in interest_df.iterrows():
        
        date, value = row[0], row[1] # date : datetime / interest : pandas series.
        value = value.to_dict()
        interest = Interest(date=date, interest=value["Etsy"])
        
        db.session.add(interest)
        db.session.commit()


def _add_interest_to_db(form):
    """For real-time option."""
    
    interest = TrendReq(hl='en-US', tz=360) # connect to google trends
        
    kw_list = form.company.data

    time_frame_dict = { '1y' : 'today 12-m', '5y' : 'today 5-y'}
    time_frame = time_frame_dict.get(form.time_frame.data)

    interest.build_payload(kw_list, timeframe=time_frame) # build pay load

    # returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.
    # return type : pandas dataframe
    interest_df = interest.interest_over_time() 
    interest_df = interest_df.iloc[:,:1] # get rid of isPartial column

    kw = kw_list[0] 

    for row in interest_df.iterrows():
        
        date, value = row[0], row[1] # date : datetime / interest : pandas series.
        value = value.to_dict()

        interest = Interest(date=date, interest=value[kw])
        interest.company = Company.query.filter_by(name=form.company.data).first()
        
        db.session.add(interest)
        db.session.commit()

    return render_template("test.html")
    

if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_interests()


