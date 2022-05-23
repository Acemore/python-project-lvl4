### Hexlet tests and linter status:
[![Actions Status](https://github.com/Acemore/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/Acemore/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/32fca9350ae1cb035763/maintainability)](https://codeclimate.com/github/Acemore/python-project-lvl4/maintainability)
[![tests-and-linter-check](https://github.com/Acemore/python-project-lvl4/actions/workflows/tests_and_linter.yml/badge.svg)](https://github.com/Acemore/python-project-lvl4/actions/workflows/tests_and_linter.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/32fca9350ae1cb035763/test_coverage)](https://codeclimate.com/github/Acemore/python-project-lvl4/test_coverage)

**Task Manager** is web app for task management using statuses and labels. Registration and authentication are required to work with the system. 

## Deployment

**Task manager** is deployed on **Heroku**:

https://acemore-task-manager.herokuapp.com/

## To run **Task Manager**

Clone repo:

```bash
git clone git@github.com:Acemore/python-project-lvl4.git
```

Create .env file in root dir and add local variables: 

```
ACCESS_TOKEN=<token from Rollbar error tracker>
DEBUG=True
SECRET_KEY=<your secret here there>
```

Install dependencies:

```bash
make install
```

Start migrations:

```bash
make migrate
```

Launch server with the app:

```bash
make run
```

Go to address http://localhost:8000/ or http://127.0.0.1:8000/
