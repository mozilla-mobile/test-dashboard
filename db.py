import os
import yaml
import pymysql
from flask import jsonify


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


file_routes = 'routes.yaml'


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        #if os.environ.get('GAE_ENV') == 'standard':
        conn = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name,
                            cursorclass=pymysql.cursors.DictCursor
                            )
        return conn
    except pymysql.MySQLError as e:
        print(e)
        
        
def lookup_sql_by_route(route, my_args):
    
    start_date = my_args.get('start_date')
    end_date = my_args.get('end_date')
    
    try:
        with open(file_routes) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for key, value in data.items():
                if key == '/' + route:
                    return value
        return 'no route match found'
    except:
        return 'an exception occurred'


def content(urlpath, my_args):

    sql = lookup_sql_by_route(urlpath, my_args)
    
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute(sql)
        results = cursor.fetchall()
        if result > 0:
            results_json = jsonify(results)
        else:
            results_json = 'No results found!'
    conn.close()
   
    return results_json
  
