# Makefile

start: install run

install: venv
	: # Initial setup and preparation of the project for deployment
	. .venv/bin/activate && pip install -r requirements.txt
	.venv/bin/python app_install_secretfile.py
	.venv/bin/python TraveSheets/manage.py makemigrations
	.venv/bin/python TraveSheets/manage.py migrate
	.venv/bin/python TraveSheets/manage.py createsuperuser

venv:
	: # Create venv if it doesn't exist
	test -d .venv || python3.10 -m venv .venv

run:
	: # Run app
	.venv/bin/python TraveSheets/manage.py runserver 81.91.190.72:80

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

run_test:
	.venv/bin/python TraveSheets/manage.py runserver 8000
