from coin.models import BaseModel
from flask.ext.login import UserMixin, make_secure_token
from peewee import *
import bcrypt
import hashlib
from coin import bitcoin

class User(BaseModel, UserMixin):
  first_name = CharField()
  last_name = CharField()
  email = CharField()
  password = CharField()
  class Meta:
    db_table = 'user'

  @staticmethod
  def hash_password(plaintext):
    return bcrypt.hashpw(plaintext, bcrypt.gensalt())

  def set_password(self, password):
    self.password = User.hash_password(password)

  def save(self):

    had_id = self.id is not None
    response = super(User, self).save()

    # Give the user a bitcoin address.
    if not had_id:
      address = bitcoin.getnewaddress(str(self.id))

    return response

  def send_money(self, to, amount):
    return bitcoin.sendtoaddress(to, amount)


  def get_transactions(self):
    transactions = bitcoin.listtransactions(
      str(self.id)
    )
    t = []
    for transaction in transactions:

      # Get the transaction id.
      try:
        txid = transaction.txid
      except:
        txid = None

      # Get the confirmations.
      try:
        confirmations = transaction.confirmations
      except:
        confirmations = None

      t.append({
        'time': transaction.time,
        'category': transaction.category,
        'amount': str(transaction.amount),
        'txid': txid,
        'confirmations': confirmations
      })

    return t

  def get_addresses(self):
    return bitcoin.getaddressesbyaccount(str(self.id))

  def get_balance(self):
    return bitcoin.getbalance(str(self.id))

  def get_public_data(self):
    data = super(User, self).get_public_data()
    data['addresses'] = self.get_addresses()
    data['balance'] = str(self.get_balance())
    data['gravatar'] = hashlib.md5(self.email.lower()).hexdigest()
    data.pop('id')
    data.pop('password')
    return data
