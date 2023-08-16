FROM python:3

WORKDIR /e2e-tests
COPY ./requirements.txt /e2e-tests/
COPY . /e2e-tests/

RUN pip install -r ./requirements.txt

# Installing google chrome
# There will be an error with status 127
# and forced exit from Chrome drive without it
RUN apt-get install -y wget
# update for downloading the chrome dependencies
RUN apt-get update
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

CMD ["pytest"]
