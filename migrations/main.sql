"define postgres chema"
SET search_path to public;

" Сreate table university"
" university_pk marked as PK to university_id"
CREATE TABLE university(
    university_id integer NOT NULL,
    university_name varchar(255),
    logo varchar(255),
    CONSTRAINT university_pk PRIMARY KEY (university_id));

"/////////////////////////////////////////////////////////////////////////"
"Create table student"
" student_pk marked as PK to faculty_id"
CREATE TABLE student (
    student_id integer NOT NULL,
    full_name varchar(255),
    telephone_number varchar(255),
    faculty_id integer,
    user_id integer,
    CONSTRAINT student_pk PRIMARY KEY(student_id));

"Mark faculty_id as FK to faculty(faculty_id)"
ALTER TABLE student ADD CONSTRAINT student_faculty_fk FOREIGN KEY (faculty_id)
REFERENCES faculty(faculty_id)
MATCH FULL
ON DELETE CASCADE
ON UPDATE CASCADE 


"Mark student_user_fk as FK to user(user_id)"
ALTER TABLE student ADD CONSTRAINT student_user_fk FOREIGN KET (user_id)
REFERENCES user(user_id)
MATCH FULL
ON DELETE CASCADE
ON UPDATE CASCADE 

"/////////////////////////////////////////////////////////////////////////"
" Сreate table faculty"
" faculty_pk marked as PK to faculty_id"
CREATE TABLE faculty(
    faculty_id integer NOT NULL,
    name varchar(255),
    shortname varchar(20),
    main_email varchar(50),
    hostel_email varchar(50),
    university_id integer,
    CONSTRAINT faculty_pk PRIMARY KEY (faculty_id));

"Mark faculty_university_fk as a FK to university_id"
ALTER TABLE faculty ADD CONSTRAINT faculty_university_fk FOREIGN KEY (university_id)
REFERENCES university (university_id) 
MATCH FULL
ON DELETE CASCADE 
ON UPDATE CASCADE;

"/////////////////////////////////////////////////////////////////////////"
"Create table user"
"user_pk as PK to user_id"
"user_id is serial for generated ID"
"is_active BOOLEAN BY DEFAULT FALSE"
CREATE TABLE user(
    user_id integer,
    login varchar(50),
    password varchar(50),
    last_visit timestamptz, 
    email varchar(100),
    role_id integer,
    faculty_id integer, 
    is_active BOOLEAN BY DEFAULT FALSE,
    CONSTRAINT user_pk PRIMARY KEY(user_id));


CREATE SEQUENCE 

"Mark user_faculty_fk as FK to faculty(faculty_id)"
ALTER TABLE user ADD CONSTRAINT user_faculty_fk FOREIGN KEY(faculty_id)
REFERENCES faculty(faculty_id)
MATCH FULL
ON DELETE CASCADE
ON UPDATE CASCADE


"/////////////////////////////////////////////////////////////////////////"
"Create table role"
CREATE TABLE role(
    role_id integer,
    role_name varchar(50));


"Mark user_role_fk as FK to role(role_id)"
ALTER TABLE user ADD CONSTRAINT user_role_fk FOREIGN KEY(role_id)
REFERENCES role(role_id)
MATCH FULL
ON DELETE CASCADE
ON UPDATE CASCADE 


"/////////////////////////////////////////////////////////////////////////"
"Create table actions"
CREATE TABLE action(
    role_id integer, 
    action_name varchar(50),
    action_id integer
    CONSTRAINT action_pk PRIMARY KEY(actione_id));