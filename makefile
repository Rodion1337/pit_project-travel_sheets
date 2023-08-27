# Makefile

start: install run

install: venv migration
	: # Activate venv and install smthing inside
	. .venv/bin/activate && pip install -r requirements.txt

venv:
	: # Create venv if it doesn't exist
	test -d .venv || python3.10 -m venv .venv

run:
	: # Run app
	.venv/bin/python TraveSheets/manage.py runserver 192.168.1.5:8000

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete
	find TraveSheets -iname __pycache__ -delete

migration: venv
	: #create and run migrations
	.venv/bin/python TraveSheets/manage.py makemigrations
	.venv/bin/python TraveSheets/manage.py migrate

lint: venv
	pip freeze > requirements.txt
	black .
	isort .
	# autopep8 ./ --recursive --in-place -a
