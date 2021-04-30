#! /usr/bin/env python
"""
Flask module providing dynamic API routing
"""

from flask import Flask, request
from db import content


app = Flask(__name__)


@app.route('/')
def home_page():
    return '<html><a href="https://github.com/mozilla-mobile/test-dashboard/blob/master/routes.yaml">ROUTES</a></html>'


@app.route('/<path:urlpath>', methods=['GET'])
def page_content(urlpath):
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    """

    return content(urlpath, request.args)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
