class DefaultConfig(object):

  DEBUG = True

  HOST = '0.0.0.0'
  PORT = 9000

  SECRET_KEY= 'super-secret-secure-key'

  # MYSQL
  MYSQL_HOST     = 'localhost'
  MYSQL_USER     = 'root'
  MYSQL_PASSWORD = 'root'
  MYSQL_DATABASE = 'coin'

  # RPC BTC/DOGE server
  RPC_USER = 'rpcuser'
  RPC_PASSWORD = 'rpcpassword'
  RPC_HOST = 'localhost'
  RPC_PORT =22555
