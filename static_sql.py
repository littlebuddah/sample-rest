"""External module with all static SQL
"""

SQL = {"owners": """CREATE TABLE IF NOT EXISTS owners
                      (owner_id TEXT PRIMARY KEY,
                       owner_username TEXT
                      );
                   """,
       "projects":
           """CREATE TABLE IF NOT EXISTS projects
              (project_id TEXT PRIMARY KEY,
              owner_id TEXT,
              project_name TEXT,
              CONSTRAINT fk_users
              FOREIGN KEY (owner_id) REFERENCES owners(owner_id)
              ON DELETE CASCADE
              );
            """,
       "comments":
           """CREATE TABLE IF NOT EXISTS comments
                (comment_id TEXT PRIMARY KEY,
                commenter_id TEXT,
                commenter_username TEXT,
                project_id TEXT,
                message TEXT,
                CONSTRAINT fk_users_projects
                FOREIGN KEY(project_id) REFERENCES projects(project_id)
                ON DELETE CASCADE
                );
           """,
       "v_owner_comments":
           """CREATE VIEW IF NOT EXISTS v_owner_project_comments AS
                SELECT *
                FROM owners
                INNER JOIN projects ON owners.owner_id = projects.owner_id
                INNER JOIN comments ON projects.project_id = comments.project_id;
             """
       }
