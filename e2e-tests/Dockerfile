FROM python:3.12-slim

# PYTHONDONTWRITEBYTECODE don't write .pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /e2e-tests/
RUN pip install -r /e2e-tests/requirements.txt
COPY . /e2e-tests/

WORKDIR /e2e-tests
CMD ["pytest", "--junitxml=../test-results/pytest-e2e.xml"]
