from flask import Flask

app = Flask(__name__)

from app.routes import general, users, categories, records
