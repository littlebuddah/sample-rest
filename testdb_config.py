"""test configuration / setup
"""

DATABASE = "sample-rest.db"
USERNAME_1 = "challengeuser1"
USERNAME_2 = "challengeuser2"
USERNAME_3 = "newuser3"
USERNAME_4 = "commenter1"
USER_UUID_1 = "8bde3e84-a964-479c-9c7b-4d7991717a1b"
USER_UUID_2 = "45e3c49a-c699-405b-a8b2-f5407bb1a133"
USER_UUID_3 = "45e3c49a-c699-405b-a8b2-somestuff"
USER_UUID_4 = "8bde3e84-a964-479c-9c7b-commenter"
MOCK_PROJ_UUID_11 = "MOCK_PROJ_UUID_11"
MOCK_PROJ_UUID_12 = "MOCK_PROJ_UUID_12"
MOCK_PROJ_UUID_21 = "MOCK_PROJ_UUID_21"
MOCK_PROJ_UUID_31 = "MOCK_PROJ_UUID_31"
PROJECT_11 = "Human Gee, Gnome"
PROJECT_12 = "Argle-Bargle"
PROJECT_21 = "Garden Shed"
PROJECT_31 = "Colossus The Forbin Project"
MOCK_COMMENT_UUID_11 = "MOCK_COMMENT_UUID_11"
MOCK_COMMENT_UUID_12 = "MOCK_COMMENT_UUID_12"
MOCK_COMMENT_UUID_21 = "MOCK_COMMENT_UUID_21"
MOCK_COMMENT_UUID_31 = "MOCK_COMMENT_UUID_31"

TEST_ROWS = \
    {
        'owners':
            {
                'insert':
                    """
                    INSERT INTO owners
                      (owner_id, owner_username)
                       VALUES(?,?);
                     """,
                'data':
                    (
                        (USER_UUID_1, USERNAME_1),
                        (USER_UUID_2, USERNAME_2),
                        (USER_UUID_3, USERNAME_3),
                        (USER_UUID_4, USERNAME_4)
                    )
            },
        'projects':
            {
                'insert':
                    """
                    INSERT INTO projects
                      (project_id, owner_id, project_name)
                       VALUES(?,?,?);
                     """,
                'data':
                    (
                        (MOCK_PROJ_UUID_11, USER_UUID_1, PROJECT_11),
                        (MOCK_PROJ_UUID_12, USER_UUID_1, PROJECT_12),
                        (MOCK_PROJ_UUID_21, USER_UUID_2, PROJECT_21),
                        (MOCK_PROJ_UUID_31, USER_UUID_3, PROJECT_31)
                    )
            },
        'comments':
            {
                'insert':
                    """
                    INSERT INTO comments
                      (comment_id, commenter_id, commenter_username, project_id, message) 
                       VALUES(?,?,?,?,?);
                     """,
                'data':
                    (
                        (MOCK_COMMENT_UUID_11, USER_UUID_1, USERNAME_1, MOCK_PROJ_UUID_11, "Owner 1, project 1, comment 1"),
                        (MOCK_COMMENT_UUID_12, USER_UUID_1, USERNAME_1, MOCK_PROJ_UUID_11, "Owner 1, project 1, comment 2"),
                        (MOCK_COMMENT_UUID_21, USER_UUID_2, USERNAME_2, MOCK_PROJ_UUID_21, "Owner 2, project 2, comment 1"),
                        (MOCK_COMMENT_UUID_31, USER_UUID_3, USERNAME_3, MOCK_PROJ_UUID_31, "Owner 3, project 1, comment 1")
                    )
            }
    }


