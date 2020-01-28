# Rest Example App

Ed Doxtator: doc6502@yahoo.com, 312-375-7334

# Usage

How to run the service app (will be available at localhost port 5000):

from the command line:

```
cd <wherever-the-app-resides>
make run # run the Flask app
make clean # cleanup extraneous files
make test_components # test the db.py and api.py modules
make test # tests the app with the test example
```

# File Descriptions

| File | Description |
|---|---|
| `Makefile` | Simple Makefile to interact with provided submitted code |
| `README` | Overview of the app and instructions for execution |
| `__init__.py` | Python namespace init |
| `app.py`  | Code for the Flask application. |
| `auth.py` | Mock auth service with hard coded user and token information. |
| `db.py` | Backend database component for the app. |
| `sample.postman_collection.json` | A collection of postman 2.1 requests to exercise the ReST endpoints |
| `requirements.txt` | List of python requirements to be installed via pip. |
| `static_sql.py` | Contains the SQL declarations for tables |
| `test_api.py` | Unit tests for `api.py` |
| `test_app.py` | Unit tests for the app.py component |
| `test_client.py` | Test code for a requests based test client. |
| `test_db.py` | Unit tests for `db.py` |
| `testdb_config.py` | Configuration data for unit tests |

# Explanation of changes

## `README`

* Reformatted to use Markdown

## `__init__.py`

No Python directory should be without one

## `Makefile`

* Added `test_components` section for backend components (db, api)

## `db.py`

Refactored:

* Updated SQL to support project requirements by adding owners, projects, and comments tables
* Externalized all static SQL statements to static_sql.py
* External SQL now does CREATE TABLE now does IF EXISTS check. DROP the individual changed tables, run `db.initialize_db()` to recreate missing tables
* Added CRUD functions for owners, projects, comments
* Added test_db.py, unittest for db.py

## `api.py`

New module, contains the API (application code). This is a separate layer that isolates the app from the database.

## `app.py`

Modified to support the endpoints in the spec.

Additionally, a new endpoint has been created `populate_test_data`. This endpoint can be accessed with a `GET`, and replaces the existing data in the `owners`, `projects`, `comments` tables with test data found in `testdb_config.py` file.

## Postman
If you use Postman, I included `sample.postman_collection.json`, which is a collection of preset HTTP calls that hit the app endpoints.  You need Postman 2.1 or later to import these calls. The calls are in a group collection called `sample`.



