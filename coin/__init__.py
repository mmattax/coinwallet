from flask import Flask, render_template, g
from flask.ext.login import LoginManager
from flask_peewee.db import Database
import bitcoinrpc
import bitcoinrpc.config

app = Flask(__name__)
app.config.from_object('coin.config.DefaultConfig')

# MySQL
app.config['DATABASE'] = {
  'engine': 'peewee.MySQLDatabase',
  'name': app.config['MYSQL_DATABASE'],
  'user': app.config['MYSQL_USER'],
  'passwd': app.config['MYSQL_PASSWORD'],
  'host': app.config['MYSQL_HOST'],
  'threadlocals': True,
}

db = Database(app)
bitcoin = bitcoinrpc.connect_to_remote(
    app.config['RPC_USER'],
    app.config['RPC_PASSWORD'],
    app.config['RPC_HOST'],
    app.config['RPC_PORT']
)

# Flask-Login
login_manager = LoginManager()
login_manager.session_protection = None
login_manager.init_app(app)

# Register blueprints
from views.site import site
from views.api import api
app.register_blueprint(site)
app.register_blueprint(api)

@login_manager.user_loader
def load_user(user_id):
  from coin.models.user import User
  try:
    return User.get(User.id == user_id)
  except:
    return None

