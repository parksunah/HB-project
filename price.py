import pandas_datareader.data as web
import pandas as pd
from model import User, Company, Following, StockPrice, Interest, connect_to_db, db

from flask import Flask
from server import app
import datetime
from dateutil.relativedelta import relativedelta


end = datetime.datetime.today()
start = end - relativedelta(years=1)
price_df = web.DataReader("ETSY", "iex", start, end)
price_df = price_df.iloc[:,3] # get rid of other columns without close price.
print(price_df)

def load_stock_prices():

    for i in range(len(price_df)):

        date = price_df.index[i] # type : pandas series.
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        value = price_df.get(price_df.index[i])
        
        stock_price = StockPrice(date=date, price=value)

        db.session.add(stock_price)
        db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

#     # In case tables haven't been created, create them
    db.create_all()

    Import different types of data
    load_stock_prices()

