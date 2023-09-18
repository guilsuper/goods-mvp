FROM selenium/standalone-chrome

WORKDIR /e2e-tests
COPY ./requirements.txt /e2e-tests/
COPY . /e2e-tests/

# Docker fails with permission denied without it
USER root
RUN apt update
RUN apt install -y python3-pip
# Needed for psycopg2 package
RUN apt install -y libpq-dev

RUN pip install -r ./requirements.txt

CMD ["pytest", "-s", "--junitxml=../test-results/pytest-e2e.xml"]
