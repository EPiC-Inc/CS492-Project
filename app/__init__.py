from flask import Flask

app = Flask(__name__)
# app.url_map.host_matching = True    # This lets it support multiple sites

from . import routes