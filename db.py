#! /usr/bin/env python
"""
Serve database content to Flask API
"""

import os
import logging

import pymysql
from flask import jsonify
import yaml


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


file_routes = 'routes.yaml'


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        # if os.environ.get('GAE_ENV') == 'standard':
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name,
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except pymysql.MySQLError as e:
        print(e)


def lookup_sql_by_route(route, my_args):

    """
    start_date = my_args.get('start_date')
    end_date = my_args.get('end_date')
    """
    try:
        with open(file_routes) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for key, value in data.items():
                if key == '/' + route:
                    return value
        return 'ERROR: no route match found'
    except FileNotFoundError:
        return 'ERROR: cannot open {0}'.format(file_routes)


def content(urlpath, my_args):

    sql = lookup_sql_by_route(urlpath, my_args)

    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute(sql)
        results = cursor.fetchall()
        if result > 0:
            resp = jsonify(results)
        else:
            resp = "NO RESULTS FOUND"

    conn.close()
    data = {"data": "TBD",
            "meta": """THIS IS INTENDED TO BE A PUBLIC API:
                    https://github.com/mozilla-mobile/test-dashboard/"""}
    data["data"] = resp
    logging.warn(resp)
    return jsonify(data)
