FROM python:3.11

# PYTHONDONTWRITEBYTECODE optimizes the python execution.
# PYTHONUNBUFFERED to see the Django logs in the console.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend
COPY ./requirements.txt /backend/
RUN pip install -r requirements.txt

# get cloud-sql-proxy in place so we can use it in the predeploy step to migrate the database
RUN curl -o /usr/bin/cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.1/cloud-sql-proxy.linux.amd64
RUN chmod +x /usr/bin/cloud-sql-proxy
# check the checksum of /usr/bin/cloud-sql-proxy so we know we downloaded the image we expected to
COPY ./checksums.txt /backend/
RUN sha256sum -c /backend/checksums.txt

# directory for cloud-sql-proxy to mount unix sockets into
RUN mkdir /cloudsql

COPY . /backend/

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# add entry point to migrate the database in predeploy step
COPY docker-predeploy-entrypoint.sh /docker-predeploy-entrypoint.sh
RUN chmod +x /docker-predeploy-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
