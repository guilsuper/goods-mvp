# Product MVP backend
The backend for the product mvp.

## Installation

### Clone or Download

-  Clone this repo to your local machine using
```
git clone https://github.com/freeworldcertified/fwc.git
```

### Create a virtual environment

- Go to backend folder
```
cd backend
```

- Setup virtual environment inside your project folder
```
python -m venv venv
./venv/Scripts/activate
```

### Required to install

- Project requirements:
```
pip install -r ./requirements.txt
```

### Environment

- Add the environment variables file (.env) to the project folder (/"~/fwc/backend"/).
It must contain the following settings:
```
SECRET_KEY="+6vtkpuu+#39e@sfy00(-10+6bagg6q_x3ci-v-8f8%%d#9t&u"
DEBUG=False
FRONTEND_HOST="http://localhost:3000"

EMAIL_USER = "dummy.stuff@gmail.com"
EMAIL_PASSWORD = "rcxghoyeshsiyplk"

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### How to run locally

- Start the terminal.

- Run the following command
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py runserver
```
