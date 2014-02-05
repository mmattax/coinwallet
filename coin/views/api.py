from flask import Blueprint, render_template, request
from flask.json import jsonify
from flask.ext.login import login_user, current_user, login_required
import time
from bitcoinrpc.exceptions import *
from coin.models.user import User

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def index():
  return render_template('index.html')

@api.route('/user/authenticate', methods=['POST'])
def authenticate_user():
  user = User.get(User.email == request.json['email'].lower())
  login_user(user)
  return jsonify(user.get_public_data())

@api.route('/user', methods=['POST'])
def create_user():
  user = User()
  user.first_name = request.json['first_name']
  user.last_name = request.json['last_name']
  user.email = request.json['email'].lower()
  user.set_password(request.json['password'].encode('utf-8'))
  user.save()

  return jsonify(user.get_public_data())

@api.route('/me')
@login_required
def me():
  return jsonify(current_user.get_public_data())

@api.route('/transactions')
@login_required
def transactions():
  return jsonify(transactions=current_user.get_transactions())


@api.route('/transactions', methods=['POST'])
@login_required
def send_money():
  try:
    txid = current_user.send_money(request.json['to'], request.json['amount'])
  except InvalidAddressOrKey as e:
    return jsonify(error='Invalid address or key.'), 500
  except (WalletError, InsufficientFunds) as e:
    return jsonify(error='Insufficient funds to complete transaction.'), 500

  return jsonify({
    'amount': 0 - request.json['amount'],
    'category': 'send',
    'confirmations': 0,
    'time': int(time.time()),
    'txid': txid
  });
