FROM python:3

# PYTHONDONTWRITEBYTECODE optimizes the python execution.
# PYTHONUNBUFFERED to see the Django logs in the console.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend
COPY ./requirements.txt /backend/
RUN pip install -r requirements.txt

COPY . /backend/

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
