# stage-v-group-13
stage-v-group-13 created by GitHub Classroom

Instructions:
First, download the set of files in the app
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

