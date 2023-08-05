# Product MVP backend
The backend for the product mvp.

## Installation

### Clone or Download

-  Clone this repo to your local machine using   
```
git clone https://github.com/bengarcia0407/products-prototype-backend.git
```

### Create a virtual environment

- Setup virtual environment inside your project folder
```
python -m venv venv
```

### Required to install

- Project requirements:
```
pip install -r /requirements.txt
```

### Environment

- Add the environment variables file (.env) to the project folder (/"Your app folder"/).
It must contain the following settings:
```
SECRET_KEY="YOUR VALUE"
DEBUG="YOUR VALUE"
FRONTEND_HOST="YOUR VALUE"
EMAIL_PASSWORD="YOUR VALUE"
EMAIL_USER="YOUR VALUE"
```

### How to run locally

- Start the terminal.
- Go to the directory "Your way to the project"/"Your app folder"/
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
