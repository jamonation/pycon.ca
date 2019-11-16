from flask import Flask
from socket import gethostname
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! From {}'.format(gethostname())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
