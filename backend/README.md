# Product MVP backend

The backend for the product mvp.

## Installation

### Clone or Download

- Clone this repo to your local machine using

```bash
git clone https://github.com/freeworldcertified/fwc.git
```

### Create a virtual environment

- Go to backend folder

```bash
cd backend
```

- Setup virtual environment inside your project folder

On Windows:

```bash
python -m venv venv
./venv/Scripts/activate
```

On Linux and macOS:

```bash
python -m venv venv
./venv/bin/activate
```

### Required to install

- Project requirements:

```bash
pip install -r ./requirements.txt
```

### Environment

- Add the environment variables file (.env) to the project folder (/"~/fwc/backend"/).

The file must contain the following settings:

- SECRET_KEY is a Django secret key for encrypting processes
- DEBUG is a Django application setting for the development process
- FRONTEND_HOST is a front-end host, so only this host has access to the backend
- POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
  keywords are related to Postgres Database

The .env file example:

```bash
SECRET_KEY="+6vtkpuu+#39e@sfy00(-10+6bagg6q_x3ci-v-8f8%%d#9t&u"
FRONTEND_HOST="http://localhost:3000"
DJANGO_DATABASE=develop
DEBUG=False
ALLOWED_HOST=localhost

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### How to run locally

- Start the terminal.

- Run the following command

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

### How to run tests locally

- Start the terminal.

- Go to the directory "backend/"

- Create backend/.env (see above)

- Run the following commands

```bash
python -m venv venv
./venv/Scripts/activate
pip install -r ./requirements.txt
pytest --junitxml=../test-results/pytest.xml  --cov --cov-report=xml:../coverage-results/pytest-coverage-report.xml
```
