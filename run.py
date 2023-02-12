from app import app
from app import db
import os
from flask import Flask, render_template, redirect, request, session
from flask_session import Session


if __name__ == '__main__':
    if not os.path.exists("./app/app.db"):
    # import ipdb; ipdb.set_trace()
        print("Database doesn't exist creating new one ...")
        db.init_app(app)
        with app.app_context():
            db.create_all()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run(debug=True)
