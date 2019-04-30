from flask import render_template, request, redirect
from config import app, db
from models import User
import routes
if __name__ == "__main__":
    app.run(debug=True)