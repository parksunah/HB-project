from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Company, Following, StockPrice, Interest, connect_to_db, db
import price 
import interest 
from forms import SelectForm, RegisterForm


from pytrends.request import TrendReq
import pandas_datareader.data as web
import pandas as pd

import datetime
from dateutil.relativedelta import relativedelta


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


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == 'POST':
        
        if form.validate():
            return _add_user_to_db(form)
            
        else:
            flash("The form was not properly completed.")

    return render_template("register.html", form=form)


def _add_user_to_db(form):
    
    user = User(name=form.name.data,
                password=form.password.data,
                email=form.email.data)

    db.session.add(user)
    db.session.commit()
    
    return redirect('/')


@app.route("/login", methods =["GET"])
def user_login():
    """Display login page."""

    return render_template("login.html")


@app.route("/create_view", methods=["GET", "POST"])
def create_view():
    """For real-time option."""

    form = SelectForm(request.form)

    if request.method == 'POST':

        return interest._add_interest_to_db(form), price._add_price_to_db(form)

    return render_template("create_view.html", form=form)

  

@app.route("/test")
def _convert_interest_to_list():
    """convert the database to a list for preparing charts."""
    
    interest_list = []

    for obj in Interest.query.all():

        interest_dict = {}
        interest_dict['date'] = obj.date.isoformat()
        interest_dict['interest'] = obj.interest
        interest_list.append(interest_dict)

    return jsonify(interest_list)


@app.route("/test2")
def _convert_stock_price_to_list():
    """convert the database to a list for preparing charts."""
    
    stock_price_list = []

    for obj in StockPrice.query.all():

        stock_price_dict = {}
        stock_price_dict['date'] = obj.date.isoformat()
        stock_price_dict['interest'] = obj.price
        stock_price_list.append(stock_price_dict)

    return jsonify(stock_price_list)





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
