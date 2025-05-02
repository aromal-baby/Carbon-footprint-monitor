from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key in production

from app import routes