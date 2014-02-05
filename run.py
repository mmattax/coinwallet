#!/usr/bin/python
from coin import app as application

if __name__ == '__main__':
  application.run(
    debug=application.config['DEBUG'],
    host=application.config['HOST'],
    port=application.config['PORT']
  )
