"""
Tests for the api.py functions
"""

import unittest
import api
import db
import testdb_config as tdc


NEW_PROJECT = "Chinese Water Python"


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


def add_new_project():
    """add_new_project - helper function to add a test project
    :return:
      value from api.add_project()
    """
    owner_id = tdc.USER_UUID_1
    response = api.add_project(owner_id, NEW_PROJECT)
    return response


def get_new_project(project_id):
    """get_new_project - helper function to fetch project row
    :param project_id:
    :return:
    """
    sql = """SELECT * FROM projects
                   WHERE project_id=?;"""

    db.c.execute(sql, (project_id,))

    return db.c.fetchall()


class TestAPI(unittest.TestCase):

    def setUp(self):

        # Initialize the database (will add any missing tables)
        with db.connect_db() as conn:
            db.initialize_db(conn)
            c = conn.cursor()

            # Clear out data from previous test
            c.execute("DELETE FROM owners;")
            c.execute("DELETE FROM projects;")
            c.execute("DELETE FROM comments;")

            conn.commit()

    def tearDown(self):
        pass

    def test_add_project(self):
        """test_add_project - test adding a single project
        """
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            response = api.add_project(conn, tdc.USER_UUID_1, NEW_PROJECT)

            project_response = api.get_project(conn, response['owner_id'], response['project_id'])
            self.assertEqual(project_response["project_name"], NEW_PROJECT)

    def test_delete_project(self):
        """test_delete_project - test deleting a single project
        """
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            response = api.add_project(conn, tdc.USER_UUID_1, NEW_PROJECT)

            delete_response = api.delete_project(conn, response['owner_id'], response['project_id'])
            self.assertEqual(delete_response["owner_username"], tdc.USERNAME_1)
            self.assertEqual(len(delete_response["comments"]), 0)

    def test_add_comment(self):
        """test_add_comment - test adding a single comment
        """
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            db_add(conn, tdc.TEST_ROWS['projects'])

            response = api.add_comment(conn, tdc.USER_UUID_4, tdc.MOCK_PROJ_UUID_11,
                                       "New Test Comment")

            self.assertEqual(response["commenter_username"], tdc.USERNAME_4)
            self.assertEqual(response["message"], "New Test Comment")


if __name__ == '__main__':
    unittest.main()
