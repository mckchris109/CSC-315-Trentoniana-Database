# stage-v-group-13
stage-v-group-13 created by GitHub Classroom

Instructions:

First, download the set of files in the app folder. That includes the SQL code, the app code, and the CSV files.

Next enter postgres using the following command

$sudo -u postgres psql

Then alter role to superuser and run the following commands.

postgres=# alter role lionsuperuser;

postgres=# \q

$psql project

project=# create extension "tablefunc";

CREATE EXTENSION

project=# create extension "dict_xsyn";

CREATE EXTENSION

project=# create extension "fuzzystrmatch";

CREATE EXTENSION

project=# create extension "pg_trgm";

CREATE EXTENSION

project=# create extension "cube";

CREATE EXTENSION

Next run the .sql file with the SQL commands to populate the table.

Next part is running the server.

ONE TIME SETUP

set the postgreSQL password for user 'lion'

sudo -u postgres psql

ALTER USER lion PASSWORD 'lion';
    
\q

install pip for Python 3

sudo apt update

sudo apt install python3-pip

install psycopg2

pip3 install psycopg2-binary

install flask

pip3 install flask

logout, then login again to inherit new shell environment

HOW TO RUN

export FLASK_APP=app.py 

flask run

then browse to http://127.0.0.1:5000/





