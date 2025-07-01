FROM postgres:13
COPY doc/schema.sql /docker-entrypoint-initdb.d/
