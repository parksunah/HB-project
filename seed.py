import datetime
from sqlalchemy import func

from model import User, Company, Following, StockPrice, Interest, connect_to_db, db
from flask import Flask
from server import app


def seed():
    """Set initial fake datas : Users and Companys."""

    user1 = User(name="Sunah", email="sunah@gmail.com", password="abc123")
    user2 = User(name="Seijin", email="seijin@gmail.com", password="abc456")
    company1 = Company("Snapchat")
    company2 = Company("Etsy")

    # Followings
    user1.company.append(company1) 
    user1.company.append(company2)
    user2.company.append(company1)


    db.session.add_all([user1, user2, company1, company2])
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Initiate instances.
    seed()
