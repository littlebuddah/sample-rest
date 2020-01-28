"""
Tests for the db.py functions
"""

import unittest
import sqlite3
import db
import testdb_config as tdc


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


class TestDB(unittest.TestCase):

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

    def test_get_owner(self):
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])

            result = db.get_owner(conn, tdc.USER_UUID_1)
            self.assertEqual(result[0][1], tdc.USERNAME_1)

    def test_get_owners(self):
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])

            result = db.get_owners(conn)
            self.assertEqual(result[1][1], tdc.USERNAME_2)

    def test_get_project(self):
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            db_add(conn, tdc.TEST_ROWS['projects'])

            result = db.get_project(conn, tdc.USER_UUID_1, tdc.MOCK_PROJ_UUID_12)

            self.assertEqual(result['project_id'], tdc.MOCK_PROJ_UUID_12)
            self.assertEqual(result['project_name'], tdc.PROJECT_12)


    def test_get_comment(self):
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            db_add(conn, tdc.TEST_ROWS['projects'])
            db_add(conn, tdc.TEST_ROWS['comments'])

            result = db.get_comment(conn, tdc.MOCK_COMMENT_UUID_12)
            self.assertEqual(result[0][4], "Owner 1, project 1, comment 2")

    def test_get_comments(self):
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            db_add(conn, tdc.TEST_ROWS['projects'])
            db_add(conn, tdc.TEST_ROWS['comments'])

            result = db.get_comments(conn, tdc.MOCK_PROJ_UUID_11)
            self.assertEqual(result[1][4], "Owner 1, project 1, comment 2")

    def test_get_owner_comments(self):
        with db.connect_db() as conn:
            db_add(conn, tdc.TEST_ROWS['owners'])
            db_add(conn, tdc.TEST_ROWS['projects'])
            db_add(conn, tdc.TEST_ROWS['comments'])

            result = db.get_owner_comments(conn, tdc.USER_UUID_1)
            self.assertEqual(len(result), 2)

            result = db.get_owner_comments(conn, tdc.USER_UUID_3)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][9], "Owner 3, project 1, comment 1")


if __name__ == '__main__':
    unittest.main()
