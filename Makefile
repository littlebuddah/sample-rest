venv/bin/python:
	virtualenv --python=python3 venv
	venv/bin/pip install -r requirements.txt

run: venv/bin/python
	venv/bin/python app.py

test_components: venv/bin/python
	venv/bin/python test_db.py
	venv/bin/python test_api.py

test: venv/bin/python
	venv/bin/python app.py &
	sleep 1 # give app a second to startup
	-venv/bin/python test_client.py
	pkill python

clean:
	rm -rf venv
	rm -f *.db
	rm -f *.pyc
	rm -rf __pycache__/
