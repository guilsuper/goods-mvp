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

### Load & Dump database data

- get cloud-sql-proxy

```bash
curl -o ./cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64
chmod +x ./cloud-sql-proxy
sudo mkdir /cloudsql
sudo chown 777 /cloudsql
```

- authenticate and run cloud-sql-proxy

```bash
gcloud auth application-default login
./cloud-sql-proxy --unix-socket /cloudsql fwc-alpha-website:us-east1:postgres-main-instance
```

- you can test this connection with psql (the password can be found in the
  [secret manager](/django-database-password/versions?project=fwc-alpha-website)
  under the django-database-password key

```bash
psql -U pguser -h /cloudsql/fwc-alpha-website:us-east1:postgres-main-instance -d postgres
postgres=> select * from api_origin_report;
 id | uid | uit | marketing_name | version | state | cogs | company_id | is_latest_version
----+-----+-----+----------------+---------+-------+------+------------+-------------------
  4 | ABC666 |   1 | ABC BadHammer  |       1 |     1 |  100 |          3 | f
  3 | ABC666 |   1 | ABC BadHammer  |       1 |     3 |  100 |          3 | f
(2 rows)

postgres=>
```

- adjust your backend/.env file to talk to the cloud sql

```bash
SECRET_KEY= <<< FILL ME IN from google serets >>>
DJANGO_DATABASE=production
POSTGRES_NAME=postgres
POSTGRES_USER=pguser
POSTGRES_PASSWORD= <<< FILL ME IN from google secrets >>>
POSTGRES_HOST=/cloudsql/fwc-alpha-website:us-east1:postgres-main-instance
```

- setup backend

```bash
python -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
```

- run dump data

```bash
cd backend/
python manage.py dumpdata | jq > /tmp/data.json
```

- run load data

```bash
python manage.py loaddata /tmp/data.json
System check identified some issues:
Installed 119 object(s) from 1 fixture(s)
```
