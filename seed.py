import datetime
from sqlalchemy import func

from model import User, Company, Following, StockPrice, Interest, connect_to_db, db
from flask import Flask
from server import app


def seed():
    """Set initial fake datas : Users and Companys."""

    user1 = User(name="Sunah", email="sunah@gmail.com", password="abc123")
    user2 = User(name="Seijin", email="seijin@gmail.com", password="abc456")
    
    # Companys
    Grubhub = Company("Grubhub")
    GoPro = Company("GoPro")
    Etsy = Company("Etsy")
    Netflix = Company("Netflix")
    Groupon = Company("Groupon")
    eBay = Company("eBay")

    # Followings
    user1.company.append(Etsy) 
    user1.company.append(GoPro)
    user2.company.append(eBay)


    db.session.add_all([user1, user2, Grubhub, GoPro, Etsy, Netflix, Groupon, eBay])
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Initiate instances.
    seed()
