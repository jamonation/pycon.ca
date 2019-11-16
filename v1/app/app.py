# flask imports
from flask import Flask
from socket import gethostname
from flask_session import Session

# other imports
import os
import redis

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

# setup session & db connections
redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT)

# setup flask
app = Flask(__name__)
SESSION_TYPE = 'redis'
SESSION_REDIS = redis_client
app.config.from_object(__name__)
Session(app)


@app.route('/')
def hello_world():
    return 'Hello, World! From {}'.format(gethostname())


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
