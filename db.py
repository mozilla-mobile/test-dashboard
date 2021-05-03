#! /usr/bin/env python
"""This module serves database content to Flask API"""

import os
import sys
import logging

import pymysql
from flask import jsonify
import yaml


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
BANNER = 'THIS IS INTENDED TO BE A PUBLIC API'
REPO = 'https://github.com/mozilla-mobile/test-dashboard/'
API = 'https://master-ocnlwxzr4q-uw.a.run.app'


file_routes = 'routes.yaml'


def open_connection():
    """
    Cloud SQL database connector

    :return conn: Database connection
    :rtype: pymysql connector object
    """
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name,
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except pymysql.MySQLError as e:
        logging.warn('ERROR: pymyqsl.MySQLError {0}'.format(e))
        sys.exit()


def lookup_sql_by_route(route, my_args):
    """
    Looks up SQL from corresponding URL path

    :param route: URL path
    :type: string
    :my_args: args from GET
    :type: Flask request object
    :return: SQL statement
    :rtype: string
    """
    # start_date = my_args.get('start_date')
    # end_date = my_args.get('end_date')
    try:
        with open(file_routes) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for key, value in data.items():
                if key == '/' + route:
                    return value
        logging.warn('ERROR: no route match found')
        return ''
    except FileNotFoundError:
        logging.warn('ERROR: an exception occurred')
        sys.exit()


def banner(resp):
    """
    Wraps API content in banner

    :param resp: JSON data
    :type: string
    :return: JSON data w/ banner
    :rtype: string
    """
    data = {"data": "TBD", "meta": BANNER}
    data["data"] = resp
    return jsonify(data)


def content(urlpath, my_args):
    """
    Provides API content

    :param route: URL path
    :type: string
    :my_args: args from GET
    :type: Flask request object
    :return: JSON content
    :rtype: JSON string
    """
    sql = lookup_sql_by_route(urlpath, my_args)
    conn = open_connection()

    with conn.cursor() as cursor:
        result = cursor.execute(sql)
        results = cursor.fetchall()
        if result > 0:
            resp = results
        else:
            resp = "NO RESULTS FOUND"

    conn.close()
    return banner(resp)


def content_home():
    with open(file_routes) as f:
        content = f.read().splitlines()

        body = ''
        for line in content:
            if line != '---':
                path = line.split(':')[0]
                line = '{0}{1}'.format(API, path)
                body += '<a href="{0}">{1}</a><br>'.format(line, path)

    repo = '<a href="{0}">{0}</a>'.format(REPO)
    return """<html><h1>{0}</h1>For more info: {1}<hr>
        {2}</html>""".format(BANNER, repo, body)
