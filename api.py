import flask
import utils
from flask import request, jsonify
import sqlite3

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

def dict_facotry(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask</h1><p>This is an API prototype in Python.</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 page not found</h1>", 404


@app.route('/api/v1/bookmarks/all', methods=['GET'])
def getAllBookmarks():
    return jsonify(bookmarks)

@app.route('/api/v1/books/all', methods=['GET'])
def getAllBooks(): 
    conn = sqlite3.connect('flask-in-action/books.db')
    conn.row_factory = dict_facotry
    cur = conn.cursor()
    allBooks = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(allBooks)

@app.route('/api/v1/books', methods=['GET'])
def getBookByFilter():
    queryStrings = request.args
    id = queryStrings.get('id')
    published = queryStrings.get('published')
    author = queryStrings.get('author')

    query = 'SELECT * FROM books WHERE'
    toFilter = []

    if id:
        query += ' id=? AND'
        toFilter.append(id)
    if published:
        query += ' published=? AND'
        toFilter.append(published)
    if author:
        query += ' author=? AND'
        toFilter.append(author)

    query = query[:-4] + ';'

    conn = sqlite3.connect('flask-in-action/books.db')
    conn.row_factory = dict_facotry
    cur = conn.cursor()

    results = cur.execute(query, toFilter).fetchall()
    return jsonify(results)

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