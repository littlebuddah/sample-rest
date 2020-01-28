"""
db.py: Contains the sample database code
"""
import sqlite3
import uuid
import static_sql


def connect_db():
    """connect_db - connect to the database
    (sqlite connections cannot be shared across threads)
    :return: sqlite database connection
    """
    conn = sqlite3.connect("sample-rest.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    return conn


def initialize_db(conn):
    """
    Creates tables in the database if they do not already exist.
    Make sure to clean up old .db files on schema changes.
    """
    c = conn.cursor()
    for table, sql in static_sql.SQL.items():
        try:
            c.execute(sql)
            conn.commit()
        except sqlite3.OperationalError as err:
            # ToDo: proper logging
            print(f"{table}: {err}")
            raise


def get_num_projects(conn):
    """get_num_projects - returns a count of all projects in the projects table
    :param conn: (sqlite db connection) Active connection to the database
    :return:
        dict
        {
            "project_count": <project-count>
        }
    """
    c = conn.cursor()
    sql = "SELECT COUNT(*) AS count FROM projects;"
    c.execute(sql)
    count = c.fetchall()[0][0]
    response = {"project_count": count}
    return response


def get_owner(conn, owner_id):
    """get_owner - get the owner for this owner uuid
    :param conn: (sqlite db connection) Active connection to the database
    :param owner_id: (string) owner uuid value
    :return:
        If found, the comment row corresponding to owner_uuid
        If not found, None
    """
    c = conn.cursor()
    sql = """SELECT * FROM owners
               WHERE owner_id=?;"""
    c.execute(sql, (owner_id,))
    return c.fetchall()


def get_owners(conn):
    """get_owners - get all the owner data
    :param conn: (sqlite db connection) Active connection to the database
    :return: A list of the owner rows. If no rows exist, the list is empty
    """
    c = conn.cursor()
    sql = """SELECT * FROM owners;"""
    c.execute(sql)
    return c.fetchall()


def add_project(conn, project_id, owner_id, project_name):
    """add_project - Add a new project to the projects table for this owner
    :param conn: (sqlite db connection) Active connection to the database
    :param project_id: (string) the uuid of the new project
    :param owner_id: (string) the owner of the project
    :param project_name: (string) the new project name
    :return:
        returns a dict with the following
          {"project_id": "<new-project-uuid>",
           "owner_id": "58d84c3a-053b-11e8-97ec-9cb6d0d9fd63",
           "owner_username": "<owner_username>",
           "project_name": "<project_name>",
           “comments”: []
          }
    """
    c = conn.cursor()

    rows = get_owner(conn, owner_id)

    sql = """INSERT INTO projects (project_id, 
                                   owner_id,
                                   project_name)
                        VALUES (?,?,?);"""

    c.execute(sql, (project_id, owner_id, project_name))

    conn.commit()

    result = {"project_id": project_id,
              "owner_id": owner_id,
              "owner_username": rows[0][1],
              "project_name": project_name,
              "comments": []}

    return result


def get_project(conn, owner_id, project_id):
    """get_project
    get the project data associated with this owner_id/project_id
    :param conn: (sqlite db connection) Active connection to the database
    :param owner_id: (string): the owner's uuid
    :param project_id: (string): the project's uuid
    :return:
        If found, the corresponding project row
        If not found, None
    """
    c = conn.cursor()

    sql = """SELECT * FROM projects
               WHERE owner_id=? AND project_id=?;"""
    c.execute(sql, (owner_id, project_id))

    project_rows = c.fetchall()

    if project_rows is None:
        result = {"message": "No project to delete"}

    else:
        owner_rows = get_owner(conn, owner_id)

        comment_rows = get_comments(conn, project_id)
        comment_data = []
        for comment_row in comment_rows:

            comment_data.append({"comment_id": comment_row[0],
                                 "commenter_id": comment_row[1],
                                 "commenter_username": comment_row[2],
                                 "message": comment_row[4]
                                 }
                                )

        result = {"project_id": project_id,
                  "owner_id": owner_id,
                  "owner_username": owner_rows[0][1],
                  "project_name": project_rows[0][2],
                  "comments": comment_data
                  }

    return result


def delete_project(conn, owner_id, project_id):
    """delete_project - Delete an existing project & associated comments
    :param conn: (sqlite db connection) Active connection to the database
    :param owner_id: (string) the uuid of the project owner
    :param project_id: (string) the uuid of the project to delete
    :return:
      dict containing
        {"project_id": <project_uuid>,
            "owner_id": <project_owner_uuid>,
            "owner_username": <project_owner_username>,
            "project_name": <project_name>,
            "comments":
                [{"comment_id": <deleted_comment_uuid>,
                  "commenter_id": <deleted_commenter_id>,
                   "commenter_username": <deleted_commenter_username>,
                   "message": <deleted_message>
                }]
        }
    """
    c = conn.cursor()
    owner_rows = get_owner(conn, owner_id)
    project_response = get_project(conn, owner_id, project_id)
    comment_rows = get_comments(conn, project_id)

    comments = [{"comment_id": row[0],
                 "commenter_id": row[1],
                 "commenter_username": row[2],
                 "message": row[4]}
                for row in comment_rows]

    response = {"project_id": project_id,
                "owner_id": owner_id,
                "owner_username": owner_rows[0][1],
                "project_name": project_response["project_name"],
                "comments": comments
    }

    sql = """DELETE FROM projects
               WHERE project_id=?"""

    c.execute(sql, (project_id,))

    conn.commit()

    return response


def add_comment(conn, commenter_id, project_id, message):
    """add_comment - add comment to this project for this commenter_id
    :param conn: (sqlite db connection) Active connection to the database
    :param commenter_id: (string) owner_id of commenter
    :param project_id: (string) project_id of project for new message
    :param message: (string) new comment message
    :return:
    """

    c = conn.cursor()
    sql = """INSERT INTO comments (comment_id,
                                   commenter_id,
                                   commenter_username,
                                   project_id,
                                   message)
                VALUES(?,?,?,?,?);
            """
    comment_id = str(uuid.uuid1())
    rows = get_owner(conn, commenter_id)
    commenter_username = rows[0][1]

    values = (comment_id, commenter_id, commenter_username, project_id, message)

    c.execute(sql, values)

    conn.commit()

    response = {"comment_id": comment_id,
                "commenter_id": commenter_id,
                "commenter_username": commenter_username,
                "message": message

    }

    return response


def get_comment(conn, comment_id):
    """get_comment - get the comment data associated with this user/project/comment
    :param conn: (sqlite db connection) Active connection to the database
    :param comment_id: (string) the comment's uuid
    :return:
        If found, the corresponding comment row
        If not found, None
    """
    c = conn.cursor()
    sql = """SELECT * FROM comments
               WHERE comment_id=?;"""
    c.execute(sql, (comment_id,))
    return c.fetchall()


def get_comments(conn, project_id):
    """get_comments - get all comment data associated with this project_id
    :param conn: (sqlite db connection) Active connection to the database
    :param project_id: (string) the project's uuid
    :return:
        If found, all corresponding comment rows
        If not found, None
    """
    c = conn.cursor()
    sql = """SELECT * FROM comments
               WHERE project_id=?;"""
    c.execute(sql, (project_id,))
    return c.fetchall()


def get_owner_comments(conn, owner_id):
    """get_owner_comments - gets all comments for the project by the project owner
    :param conn: (sqlite db connection) Active connection to the database
    :param owner_id:
    :return:
        If found, all corresponding comment rows
        If not found, None
    """
    c = conn.cursor()
    sql = """SELECT * FROM v_owner_project_comments
               WHERE owner_id=?;"""
    c.execute(sql, (owner_id,))
    return c.fetchall()

