"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json
from flask import Flask, request, Response, abort

import api
import db
import sqlite3
from auth import introspect_token

app = Flask(__name__)


def db_add(conn, sql_dict):
    """db_add - add test data to the table in sql_dict
    :param conn: (sqlite db connection) Active connection to the database
    :param sql_dict: (dict) contains INSERT statement and test data tuples
    :return: None
    """
    c = conn.cursor()
    sql = sql_dict["insert"]
    for data in sql_dict['data']:
        try:
            c.execute(sql, data)
            conn.commit()
        except (sqlite3.OperationalError,
                sqlite3.ProgrammingError,
                sqlite3.IntegrityError) as err:
            print(f"{err}\n{sql}\n{str(data)}")
            raise


def auth_bearer_token(request):
    """auth_bearer_token - authenticate the user in the bearer token
    :param request: Flask request, containing bearer token in head
    :return:
       If valid, token_info structure for this user
       If invalid, return 401 to caller
    """
    # get bearer token from auth header
    auth_header = request.headers.get("authorization")
    access_token = auth_header[len("Bearer "):]

    # get user_info to respond with
    token_info = introspect_token(access_token)
    if not token_info["token_is_valid"]:
        abort(401)

    return token_info["user_info"]


@app.errorhandler(401)
def custom_401(error):
    """custom_401 - custom error handler for HTTP 401
    :param error: flask error object
    :return: payload containing 401 error
    """
    return Response('Invalid user',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/app/populate_test_data", methods=["GET"])
def populate_test_data():
    """populate_test_data - clears the old data, and adds a fresh test dataset
    :return:
    """
    import testdb_config as tdc
    with db.connect_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM owners;")
        c.execute("DELETE FROM projects;")
        c.execute("DELETE FROM comments;")
        conn.commit()
        db_add(conn, tdc.TEST_ROWS['owners'])
        db_add(conn, tdc.TEST_ROWS['projects'])
        db_add(conn, tdc.TEST_ROWS['comments'])

    return Response(json.dumps({"message": "OK"}), status=200,
                    mimetype='application/json')


@app.route("/projects/count", methods=["GET"])
def get_projects_count():
    """get_projects_count - get a count of all projects
    Does not handle missing or invalid Access Tokens
    """

    # Authenticate user
    user_info = auth_bearer_token(request)
    username = user_info["username"]

    if request.method == "GET":
        with db.connect_db() as conn:
            response = api.get_num_projects(conn)

        response = {"message":
                        f"""Hello {username}, there are {response["project_count"]} projects in the database!"""
        }

    return Response(json.dumps(response), status=200,
                    mimetype='application/json')


@app.route("/projects", methods=["POST"])
def add_project():
    """ add_project - Add project to projects table
    :return: JSON containing owner, project, comment info
    """

    # Authenticate user
    user_info = auth_bearer_token(request)
    user_id = user_info["user_id"]

    request_json = request.get_json()

    with db.connect_db() as conn:
        if request.method == "POST":
            response = api.add_project(conn, user_id, request_json["project_name"])

    return Response(json.dumps(response),
                    status=200, mimetype='application/json')


@app.route("/projects/<project_id>", methods=["GET", "DELETE"])
def projects(project_id):
    """get_project - handle GET and DELETE project requests
    :param project_id: (string) the uuid of the project to GET or DELETE
    :return:
    """

    # Authenticate user
    user_info = auth_bearer_token(request)
    user_id = user_info["user_id"]

    with db.connect_db() as conn:
        if request.method == "GET":
            response = api.get_project(conn, user_id, project_id)

        elif request.method == "DELETE":
            response = api.delete_project(conn, user_id, project_id)

    return Response(json.dumps(response),
                    status=200, mimetype='application/json')


@app.route("/projects/<project_id>/comments", methods=["POST"])
def add_comment(project_id):
    """add a comment to a user's project.
    :param project_id: (string) uuid of the project to add the comment
    :return:
    """

    # Authenticate user
    _ = auth_bearer_token(request)

    response = {}

    request_json = request.get_json()
    with db.connect_db() as conn:
        if request.method == "POST":
            response = api.add_comment(conn,
                                       request_json['commenter_id'],
                                       project_id,
                                       request_json['message'])

    return Response(json.dumps(response),
                    status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
