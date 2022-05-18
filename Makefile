MANAGE := poetry run python manage.py

lint:
	poetry run flake8 task_manager

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

requirements:
	poetry export -f requirements.txt --output requirements.txt

run:
	$(MANAGE) runserver

test:
	poetry run coverage run manage.py test task_manager.users.tests
	poetry run coverage run manage.py test task_manager.statuses.tests
	poetry run coverage run manage.py test task_manager.tasks.tests
	poetry run coverage run manage.py test task_manager.labels.tests

test-coverage:
	make test
	poetry run coverage xml
	poetry run coverage report

.PHONY: lint run test
