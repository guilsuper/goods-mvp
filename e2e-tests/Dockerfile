FROM python:3

WORKDIR /e2e-tests
COPY ./requirements.txt /e2e-tests/
COPY . /e2e-tests/

RUN pip install -r ./requirements.txt

# Installing google chrome
# There will be an error with status 127
# and forced exit from Chrome drive without it
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

CMD ["pytest"]
