FROM selenium/standalone-chrome

# Docker fails with permission denied without it
USER root
RUN apt-get update
RUN apt-get install -y python3-pip

COPY ./requirements.txt /e2e-tests/
RUN pip install -r /e2e-tests/requirements.txt
COPY . /e2e-tests/

WORKDIR /e2e-tests
CMD ["pytest", "--junitxml=../test-results/pytest-e2e.xml"]
