"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy



# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    company = db.relationship("Company", secondary="followings", backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} name={self.name} email={self.email}>"



class Following(db.Model):
    """User's following companys."""

    __tablename__ = "followings"

    following_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    company_id = db.Column(db.Integer, db.ForeignKey("companys.company_id"))


class Company(db.Model):
    """Company searching for."""

    __tablename__ = "companys"

    company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Company company_id={self.company_id} name={self.name}>"


class StockPrice(db.Model):
    """Stock price on database."""

    __tablename__ = "stock_prices"

    stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companys.company_id"))
    
    company = db.relationship("Company", backref=db.backref("stock_prices"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<StockPrice stock_id={self.stock_id}, date={self.date}, price={self.price}, company_id={self.company_id}>"



class Interest(db.Model):
    """Interest from google trends."""

    __tablename__ = "interests"

    interest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    interest = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companys.company_id"))

    company = db.relationship("Company", backref=db.backref("interests"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Interest interest_id={self.interest_id}, date={self.date}, interest={self.interest}, company_id={self.company_id}>"






##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///model"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")   

   


        
    
    
