from flask import Flask
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from dotenv import load_dotenv
import os


load_dotenv()
envs = os.environ  

def create_app():
    app = Flask(__name__)
    #more setup here
    return app


app = create_app()

cors = CORS(app)
  
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 900
}

# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

from . import rfps
app.register_blueprint(rfps.rfp)
from . import proposals
app.register_blueprint(proposals.proposals)