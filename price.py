import pandas_datareader.data as web
import pandas as pd

from flask import Flask, render_template, redirect, request, flash, session, url_for

import datetime
from dateutil.relativedelta import relativedelta

from model import User, Company, Following, StockPrice, Interest, connect_to_db, db
from forms import SelectForm, RegisterForm


end = datetime.datetime.today()
start = end - relativedelta(years=1)
price_df = web.DataReader("ETSY", "iex", start, end)
price_df = price_df.iloc[:,3] # get rid of other columns without close price.

def load_stock_prices():

    for i in range(len(price_df)):

        date = price_df.index[i] # type : pandas series.
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        value = price_df.get(price_df.index[i])

        stock_price = StockPrice(date=date, price=value)

        db.session.add(stock_price)
        db.session.commit()


def _add_price_to_db(form):
    """For real-time option."""
    
    end = datetime.datetime.today()
    start = end - relativedelta(years=1)
    price_df = web.DataReader("ETSY", "iex", start, end)
    price_df = price_df.iloc[:,3] # get rid of other columns without close price.

    for i in range(len(price_df)):

        date = price_df.index[i] # type : pandas series.
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        value = price_df.get(price_df.index[i])

        stock_price = StockPrice(date=date, price=value)

        db.session.add(stock_price)
        db.session.commit()

        stock_price.company = Company.query.filter_by(name=form.company.data).first()


    return render_template("test.html")



if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_stock_prices()

