from flask import Flask
from dotenv import load_dotenv
from app.config.devConfig import DevConfig
from app.routes.v1 import v1

def createServer():
    load_dotenv()
    app = Flask(__name__)

    app.env = DevConfig().ENV
    app.register_blueprint(v1, url_prefix = "/v1")

    return app


if __name__ == '__main__':
    app = createServer()
    app.run(host=DevConfig().HOST, port=DevConfig().PORT)