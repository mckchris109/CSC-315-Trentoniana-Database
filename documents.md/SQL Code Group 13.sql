create extension "tablefunc";
create extension "dict_xsyn";
create extension "fuzzystrmatch";
create extension "pg_trgm";
create extension "cube";

DROP TABLE information;
DROP TABLE users;
DROP TABLE admins;
DROP TABLE user_update;

CREATE TABLE information (
jhs_name char(100) PRIMARY KEY,
sound_name char(100),
sound_link char(100),
transcript char(100));

COPY information (jhs_name, sound_name, sound_link, transcript)
FROM '/home/lion/work/project/Trentoniana.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM information;

CREATE TABLE users (
id SERIAL PRIMARY KEY,
date char(20));

COPY users (date)
FROM '/home/lion/work/project/Users.csv'
DELIMITER ','
CSV HEADER;
SELECT * FROM USERS;

CREATE TABLE admins (
email varchar PRIMARY KEY,
fname char(20),
lname char(50),
password char(20));

COPY admins (email,fname,lname,password)
FROM '/home/lion/work/project/Admin.csv'
DELIMITER ','
CSV HEADER;
SELECT * FROM admins;

CREATE TABLE user_update (
update_id SERIAL PRIMARY KEY,
status varchar DEFAULT 'waiting',
proposed_change varchar);

COPY user_update (status, proposed_change)
FROM '/home/lion/work/project/updates.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM user_update;

UPDATE information
SET sound_name = 'John Doe (JHS12)'
WHERE jhs_name = 'JHS 12';

SELECT * FROM information;

DELETE FROM information
WHERE jhs_name = 'JHS 12';

SELECT * FROM information;

INSERT INTO information (jhs_name, sound_name, sound_link, transcript)
VALUES ('JHS 12','Barker, Maynard (JHS12)','https://archive.org/details/JHS05SideA','https://trentonlib.org/wp-content/uploads/2021/02/JHS-12-Barker.pdf');

SELECT * FROM information;

INSERT INTO user_update (proposed_change)
VALUES ('JHS 12 name should not be John Doe');

SELECT * FROM user_update;

UPDATE user_update
SET status = 'Verified'
WHERE update_id = 4;

SELECT * FROM user_update;

SELECT *
FROM information
WHERE sound_name ILIKE 'Garfing%'
;


INSERT INTO admins (email,fname,lname,password)
VALUES ('jerry@gmail.com', 'Jerry', 'Seinfeld', 'abc');

SELECT * FROM admins;

UPDATE admins
SET password = 'def'
WHERE email = 'jerry@gmail.com';

SELECT * FROM admins;

DELETE from admins
WHERE email = 'jerry@gmail.com';

SELECT * FROM admins;
