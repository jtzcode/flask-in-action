import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask</h1><p>This is an API prototype in Python.</p>"

app.run()