#  flask imports
from flask import Flask
from socket import gethostname
from flask_session import Session
from healthcheck import HealthCheck, EnvironmentDump

# other imports
import os
import psycopg2 as db
import redis

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_NAME = os.environ['DB_NAME']
DB_PASS = os.environ['DB_PASS']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

# setup session & db connections
redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT)

db_client = db.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        database=DB_NAME)

# setup flask
app = Flask(__name__)
SESSION_TYPE = 'redis'
SESSION_REDIS = redis_client
app.config.from_object(__name__)
Session(app)

# register healthcheck & environment endpoints
health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")


@app.route('/')
def hello_world():
    return 'Hello, World! From {}'.format(gethostname())


# add healthcheck functions
def check_hostname():
    hostname = gethostname()
    return True, "{}".format(hostname)


def redis_available():
    redis_client.info()
    return True, "redis ok"


def postgres_available():
    db_client.status
    return True, "postgres ok"


health.add_check(check_hostname)
health.add_check(redis_available)
health.add_check(postgres_available)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
