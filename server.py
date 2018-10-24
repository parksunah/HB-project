from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Company, Following, StockPrice, Interest, connect_to_db, db

from forms import SelectForm


from pytrends.request import TrendReq
import pandas as pd

import datetime



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""


    return render_template("homepage.html")


@app.route("/register", methods=["GET"])
def register_form():
    """User Registration."""


    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return redirect('/')


@app.route("/login", methods =["GET"])
def user_login():
    """Display login page."""

    return render_template("login.html")


@app.route("/create_view", methods=["GET", "POST"])
def select_view():
    """Select company and period to show the correlation view."""

    form = SelectForm(request.form)

    if request.method == 'POST':

        interest = TrendReq(hl='en-US', tz=360) # connect to google trends
        
        kw_list = form.company.data
        time_frame_dict = { '1y' : 'today 12-m', '5y' : 'today 5-y'}
        time_frame = time_frame_dict.get(form.time_frame.data)

        interest.build_payload(kw_list, timeframe=time_frame) # build pay load

        # returns historical, indexed data for when the keyword was searched most as shown on Google Trends' Interest Over Time section.
        # return type : pandas dataframe
        interest_df = interest.interest_over_time() 
        interest_df = interest_df.iloc[:,:1] # get rid of isPartial column

        empty = []
        kw = kw_list[0] 

        for row in interest_df.iterrows():
            
            date, value = row[0], row[1] # date : datetime / interest : pandas series.
            value = value.to_dict()

            interest = Interest(date=date, interest=value[kw])
            
            db.session.add(interest)
            db.session.commit()     


        return render_template("test.html")

    return render_template("create_view.html", form=form)

   



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    db.create_all()

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
