import flask
import utils
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

bookmarks = [
    {
        'id': '0',
        'name': 'python',
        'children': [
            {
                'id': '00',
                'name': 'python offical',
                'link': 'https://www.python.org/'
            },
            {
                'id': '01',
                'name': 'python webapi',
                'link': 'https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask'
            }
        ]
    },
    {
        'id': '1',
        'name': 'python org',
        'link': 'https://www.python.org/'
    }
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask</h1><p>This is an API prototype in Python.</p>"

@app.route('/api/v1/bookmarks/all', methods=['GET'])
def getAllBookmarks():
    return jsonify(bookmarks)

@app.route('/api/v1/bookmarks', methods=['GET'])
def getBookmarkById():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No ID field is specified."

    results = []
    linkResults = []
    utils.flattenBookmarks(bookmarks, linkResults)
    print(f"Flatten results: {len(linkResults)}")
    for link in linkResults:
        if link['id'] == id:
            results.append(link)
    
    return jsonify(results)

app.run()