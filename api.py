"""
api.py: Contains the transformational functions required for the sample
"""

import uuid
import db


def add_project(conn, owner_id, project_name):
    """add_project - Add a new project
    :param conn: sqllite3 db connection
    :param owner_id: (string) owner's uuid
    :param project_name: (string) name of new project
    :return: a dict with the project / owner info
    """

    # Passed authorization, so add this project
    project_id = str(uuid.uuid1())
    return db.add_project(conn, project_id, owner_id, project_name)


def get_num_projects(conn):
    """get_num_project - get number of total projects
    :param conn: sqllite3 db connection
    :return:
    """
    return db.get_num_projects(conn)


def get_project(conn, owner_id, project_id):
    """get_project - get project for this project_id
    :param conn: sqllite3 db connection
    :param project_id:
    :return:
    """
    return db.get_project(conn, owner_id, project_id)


def delete_project(conn, owner_id, project_id):
    """delete_project - delete project for this project_id
    :param conn: sqllite3 db connection
    :param owner_id: (string) project owner uuid
    :param project_id: (string) project id uuid
    :return:
    """
    # Check to ensure the project owner is requesting delete
    return db.delete_project(conn, owner_id, project_id)


def add_comment(conn, commenter_id, project_id, message):
    """add_comment - add a new comment to this project
    :param conn: sqllite3 db connection
    :param commenter_id: (string) commenter uuid
    :param project_id: (string) project_id
    :param message: (string) message text
    :return:
        returns value from db.add_comment()
    """
    return db.add_comment(conn, commenter_id, project_id, message)


def update_comment(conn, comment_id, message):
    """update_comment - Update an existing comment
    :param conn: sqllite3 db connection
    :param comment_id: (string) comment uuid
    :param message: (string) message text
    :return:
    """
    return db.update_comment(conn, comment_id, message)
