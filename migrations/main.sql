-- define postgres chema"
SET search_path to public;

--Сreate table university
-- university_pk marked as PK to university_id
CREATE TABLE IF NOT EXISTS university (
    university_id integer NOT NULL,
    university_name varchar(255) NOT NULL,
    short_university_name varchar(50) NOT NULL,
    logo varchar(255),
    CONSTRAINT university_pk PRIMARY KEY (university_id));

-- Create sequence university_id_seq"
CREATE SEQUENCE IF NOT EXISTS university_id_seq AS bigint
START WITH 1 INCREMENT BY 1;

ALTER TABLE university ALTER COLUMN university_id SET DEFAULT
nextval('university_id_seq');

-- Сreate table faculty
-- faculty_pk marked as PK to faculty_id
CREATE TABLE IF NOT EXISTS faculty(
    faculty_id integer NOT NULL,
    name varchar(255) NOT NULL,
    shortname varchar(20),
    main_email varchar(50),
    university_id integer NOT NULL,
    CONSTRAINT faculty_pk PRIMARY KEY (faculty_id));

-- Create sequence faculty_id_seq
CREATE SEQUENCE IF NOT EXISTS faculty_id_seq AS bigint
START WITH 1 INCREMENT BY 1;

-- Link sequnce to column faculty_id
ALTER TABLE faculty ALTER COLUMN faculty_id SET DEFAULT
nextval('faculty_id_seq');

-- Mark faculty_university_fk as a FK to university_id"
ALTER TABLE faculty ADD CONSTRAINT faculty_university_fk 
FOREIGN KEY (university_id) REFERENCES university (university_id) 
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Create table student
-- student_pk marked as PK to faculty_id"
CREATE TABLE IF NOT EXISTS student (
    student_id integer NOT NULL,
    full_name varchar(255) NOT NULL,
    telephone_number varchar(255) NOT NULL UNIQUE,
    faculty_id integer NOT NULL,
    user_id integer,
    CONSTRAINT student_pk PRIMARY KEY(student_id));

-- Create sequence student_id_seq
CREATE SEQUENCE IF NOT EXISTS student_id_seq AS bigint
START WITH 1 INCREMENT BY 1;

-- Link sequence to column student_id
ALTER TABLE student ALTER COLUMN student_id SET DEFAULT
nextval('student_id_seq');


-- Mark student.faculty_id as FK to faculty(faculty_id)
ALTER TABLE student ADD CONSTRAINT student_faculty_fk 
FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE; 


-- Create table user
CREATE TABLE IF NOT EXISTS "user"(
    user_id integer NOT NULL,
    login varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    last_visit timestamp,
    email varchar(100) NOT NULL,
    role_id integer NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    UNIQUE (login, email),
    CONSTRAINT user_pk PRIMARY KEY(user_id));

-- Create sequence user_id_seq"
CREATE SEQUENCE IF NOT EXISTS user_id_seq AS bigint
START WITH 1 INCREMENT BY 1;

-- Link sequence to column user_id_seq
ALTER TABLE "user" ALTER COLUMN user_id SET DEFAULT
nextval('user_id_seq');

-- Mark student_user_fk as FK to user(user_id)
ALTER TABLE student ADD CONSTRAINT student_user_fk 
FOREIGN KEY (user_id) REFERENCES "user"(user_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

-- Create table role
CREATE TABLE IF NOT EXISTS role(
    role_id integer NOT NULL,
    role_name varchar(50) NOT NULL,
    CONSTRAINT role_pk PRIMARY KEY(role_id));

-- Create sequence role_id_seq"
CREATE SEQUENCE IF NOT EXISTS role_id_seq AS bigint
START WITH 1 INCREMENT BY 1;

-- Link sequence to column role_id_seq
ALTER TABLE role ALTER COLUMN role_id SET DEFAULT
nextval('role_id_seq');

-- Mark user_role_fk as FK to role(role_id)"
ALTER TABLE "user" ADD CONSTRAINT user_role_fk 
FOREIGN KEY(role_id) REFERENCES role(role_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Create table actions"
CREATE TABLE IF NOT EXISTS action(
    role_id integer NOT NULL, 
    action_name varchar(50) NOT NULL,
    action_id integer NOT NULL,
    CONSTRAINT action_pk PRIMARY KEY(action_id));

-- Create sequence action_id_seq"
CREATE SEQUENCE IF NOT EXISTS action_id_seq AS bigint
START WITH 1 INCREMENT BY 1;

-- Link sequence to column action_id_seq
ALTER TABLE action ALTER COLUMN action_id SET DEFAULT
nextval('action_id_seq');

-- Mark action_role_fk as FK to action(role(id)"
ALTER TABLE action ADD CONSTRAINT action_role_fk 
FOREIGN KEY(role_id) REFERENCES role(role_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Create table user_facultygetd
CREATE TABLE IF NOT EXISTS user_faculty(
    user_id integer NOT NULL,
    faculty_id integer NOT NULL,
    CONSTRAINT user_faculty_pk PRIMARY KEY(user_id, faculty_id));

--Mark user_faculty as FK to user(user_id)
ALTER TABLE user_faculty ADD CONSTRAINT user_faculty_user_fk 
FOREIGN KEY(user_id) REFERENCES "user"(user_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE; 

-- Mark user_faculty as FK faculty(faculty_id)
ALTER TABLE user_faculty ADD CONSTRAINT user_faculty_faculty_fk 
FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Create table one_time_tocken
CREATE TABLE IF NOT EXISTS one_time_token(
    student_id integer NOT NULL,
    token_id integer NOT NULL, 
    token varchar(255) NOT NULL, 
    expires timestamp NOT NULL,
    CONSTRAINT one_time_token_pk PRIMARY KEY (token_id));

-- Create sequence to column token_id_seq
CREATE SEQUENCE IF NOT EXISTS token_id_seq AS bigint
START WITH 1 INCREMENT BY 1; 

ALTER TABLE one_time_token ALTER COLUMN token_id SET DEFAULT
nextval('token_id_seq');

ALTER TABLE one_time_token ADD CONSTRAINT one_time_token_student_fk
FOREIGN KEY (student_id) REFERENCES student(student_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- INSERT DATA TO table university
INSERT INTO university(university_name, short_university_name)
VALUES ('Харківський національний економічний університет імені Семена Кузнеця',
        'ХНЕУ ім. С. Кузнеця');

-- INSERT DATA to table role
INSERT INTO role(role_name) VALUES ('Студент');

INSERT INTO role(role_name) VALUES ('Адміністратор');

INSERT INTO role(role_name) VALUES ('Супер Адміністратор');

DROP VIEW IF EXISTS user_list_view; 
CREATE VIEW user_list_view AS
    SELECT
        u.user_id,
        u.login,
        u.last_visit,
        u.email,
        u.is_active,
        COALESCE(json_agg(json_build_object('role', u.role_id, 'role_name', r.role_name)) FILTER (WHERE r.role_name IS NOT NULL), NULL) as role, 
        COALESCE(json_agg(json_build_object('faculty', f.faculty_id, 'faculty_name', f.name)) FILTER (WHERE f.name IS NOT NULL), NULL) as faculties,
        un.university_id
    FROM "user" u 
    LEFT JOIN "role" r ON 
        r.role_id = u.role_id 
    LEFT JOIN user_faculty uf ON 
        uf.user_id = u.user_id 
    LEFT JOIN faculty f ON 
        f.faculty_id = uf.faculty_id
    LEFT JOIN university un ON
        un.university_id = f.university_id
    GROUP BY
        u.user_id,
        u.login,
        u.last_visit,
        u.email,
        u.is_active,
        un.university_id
    ORDER BY
        un.university_id,
        u.user_id,
        u.is_active;


-- Create table service
CREATE TABLE IF NOT EXISTS service(
    service_id integer NOT NULL,
    service_name varchar(255) NOT NULL, 
    CONSTRAINT service_pk PRIMARY KEY (service_id));


INSERT INTO service(service_id, service_name) VALUES (1, 'Поселення в гуртожиток');


-- Create table status
CREATE TABLE IF NOT EXISTS status(
    status_id integer NOT NULL,
    status_name varchar(50) NOT NULL,
    CONSTRAINT status_pk PRIMARY KEY (status_id));


INSERT INTO status(status_id, status_name) VALUES (1, 'Схвалено');
INSERT INTO status(status_id, status_name) VALUES (2, 'Відхилено');
INSERT INTO status(status_id, status_name) VALUES (3, 'Розглядається');
INSERT INTO status(status_id, status_name) VALUES (4, 'Скасовано');


-- Create table user_request
CREATE TABLE IF NOT EXISTS user_request(
    user_request_id integer NOT NULL,
    faculty_id integer NOT NULL,
    university_id integer NOT NULL,
    user_id integer NOT NULL,
    service_id integer NOT NULL, 
    date_created timestamp NOT NULL, 
    status_id integer NOT NULL,
    comment VARCHAR(255),
    CONSTRAINT user_request_pk PRIMARY KEY(user_request_id));


-- Create sequence to column user_request_id
CREATE SEQUENCE IF NOT EXISTS user_request_id_seq AS bigint
START WITH 1 INCREMENT BY 1; 


ALTER TABLE user_request ALTER COLUMN user_request_id SET DEFAULT
nextval('user_request_id_seq');


-- foreign key from user_request table to service table
ALTER TABLE user_request ADD CONSTRAINT user_request_service_fk
FOREIGN KEY (service_id) REFERENCES service(service_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;


-- foreign key from user_request table to status table
ALTER TABLE user_request ADD CONSTRAINT user_request_status_fk
FOREIGN KEY (status_id) REFERENCES status(status_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;


-- foreign key from user_request table to faculty table
ALTER TABLE user_request ADD CONSTRAINT user_request_faculty_fk
FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;


-- foreign key from user_request table to faculty table
ALTER TABLE user_request ADD CONSTRAINT user_request_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;


-- foreign key from user_request table to user table
ALTER TABLE user_request ADD CONSTRAINT user_request_user_fk
FOREIGN KEY (user_id) REFERENCES "user"(user_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;


-- Create table user_document
CREATE TABLE IF NOT EXISTS user_document(
    user_document_id integer NOT NULL,
    name varchar(255) NOT NULL, 
    content varchar(255) NOT NULL, 
    date_created timestamp NOT NULL, 
    user_request_id integer NOT NULL,
    CONSTRAINT user_document_pk PRIMARY KEY (user_document_id));


-- Create sequence to column user_document_id
CREATE SEQUENCE IF NOT EXISTS user_document_id_seq AS bigint
START WITH 1 INCREMENT BY 1; 


ALTER TABLE user_document ALTER COLUMN user_document_id SET DEFAULT
nextval('user_document_id_seq');

-- INSERT DATA TO table faculty
INSERT INTO faculty(faculty_id, name, shortname, university_id)
VALUES (1, 'Інформаційних технологій', 'ІТ', 1);

INSERT INTO faculty(faculty_id, name, shortname, university_id)
VALUES (2, 'Міжнародних відносин і журналістики', 'МВЖ', 1);

INSERT INTO faculty(faculty_id, name, shortname, university_id)
VALUES (3, 'Міжнародної економіки і підприємництва', 'МЕП', 1);

INSERT INTO faculty(faculty_id, name, shortname, university_id)
VALUES (4, 'Фінансів і обліку', 'ФіО', 1);

INSERT INTO faculty(faculty_id, name, shortname, university_id)
VALUES (5, 'Менеджмента і маркетингу', 'МіМ', 1);

INSERT INTO faculty(faculty_id, name, shortname, university_id)
VALUES (6, 'Економіки і права', 'ЕіП', 1);

DROP VIEW IF EXISTS user_request_exist_view; 
CREATE VIEW user_request_exist_view AS
    SELECT
        ur.user_request_id,
        ur.user_id,
        ur.faculty_id,
        ur.university_id,
        ur.service_id,
        jsonb_build_object('status_id', ur.status_id, 'status_name', st.status_name) as status
    FROM 
        user_request ur
    LEFT JOIN status st ON
        ur.status_id = st.status_id
    WHERE
        ur.status_id in (1, 3)
    GROUP BY
        ur.user_request_id,
        ur.user_id,
        ur.faculty_id,
        ur.university_id,
        ur.service_id,
        st.status_name
    ORDER BY
        ur.university_id,
        ur.faculty_id,
        ur.user_id;

-- Create table bed_places
CREATE TABLE IF NOT EXISTS bed_places(
    bed_place_id integer NOT NULL,
    bed_place_name varchar(50) NOT NULL, 
    CONSTRAINT bed_place_pk PRIMARY KEY (bed_place_id));


-- INSERT DATA to table bed_places
INSERT INTO bed_places(bed_place_id, bed_place_name) VALUES (1, '0.75');

INSERT INTO bed_places(bed_place_id, bed_place_name) VALUES (2, '1');

INSERT INTO bed_places(bed_place_id, bed_place_name) VALUES (3, '1.5');

-- Create Table dekan
CREATE TABLE IF NOT EXISTS dekan(
    dekan_id integer NOT NULL, 
    full_name varchar(255) NOT NULL,
    CONSTRAINT dekan_pk PRIMARY KEY (dekan_id));

-- INSERT DATA to table dekan
INSERT INTO dekan(dekan_id, full_name) VALUES (1, 'Коц Григорій Павлович');

INSERT INTO dekan(dekan_id, full_name) VALUES (2, 'Птащенко Олена Валеріївна');

INSERT INTO dekan(dekan_id, full_name) VALUES (3, 'Шталь Тетяна Валеріївна');

INSERT INTO dekan(dekan_id, full_name) VALUES (4, 'Проноза Павло Володимирович');

INSERT INTO dekan(dekan_id, full_name) VALUES (5, 'Вовк Володимир Анатолійович');

INSERT INTO dekan(dekan_id, full_name) VALUES (6, 'Бріль Михайло Сергійович');


-- Add column dekan_id to table faculty
ALTER TABLE faculty ADD dekan_id integer; 

-- Mark faculty_dekan_fk as FK to dekan_id
ALTER TABLE faculty ADD CONSTRAINT faculty_dekan_fk
FOREIGN KEY (dekan_id) REFERENCES dekan(dekan_id) 
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Update in table faculty column dekan_id  
UPDATE faculty SET dekan_id = 1 WHERE faculty_id = 1;

UPDATE faculty SET dekan_id = 2 WHERE faculty_id = 2;

UPDATE faculty SET dekan_id = 3 WHERE faculty_id = 3;

UPDATE faculty SET dekan_id = 4 WHERE faculty_id = 4;

UPDATE faculty SET dekan_id = 5 WHERE faculty_id = 5;

UPDATE faculty SET dekan_id = 6 WHERE faculty_id = 6;

-- Create table rector
CREATE TABLE IF NOT EXISTS rector(
    rector_id integer NOT NULL, 
    full_name varchar(255) NOT NULL,
    CONSTRAINT rector_pk PRIMARY KEY (rector_id));

-- INSERT DATA to rector table
INSERT INTO rector(rector_id, full_name) VALUES (1, 'Пономаренко Володимир Степанович');

-- Add column rector_id to table university
ALTER TABLE university ADD rector_id integer;

-- Mark university_rector_fk as FK to rector_id
ALTER TABLE university ADD CONSTRAINT university_rector_fk
FOREIGN KEY (rector_id) REFERENCES rector(rector_id) 
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Update in table university column rector_id  
UPDATE university SET rector_id = 1 WHERE university_id = 1;

-- Create view for descibe faculty_list_view
DROP VIEW IF EXISTS faculty_list_view; 
CREATE VIEW faculty_list_view AS
    SELECT
        f.university_id,
        f.faculty_id,
        f.name,
        f.shortname,
        f.main_email,
        f.dekan_id,
        d.full_name as decan_full_name
    FROM
        faculty f
    LEFT JOIN dekan d ON
        d.dekan_id = f.dekan_id
    ORDER BY
        f.university_id,
        f.faculty_id,
        f.dekan_id;


CREATE TABLE IF NOT EXISTS speciality(
    speciality_id integer NOT NULL,
    university_id integer NOT NULL,
    code integer NOT NULL,
    name VARCHAR(255) NOT NULL, 
    CONSTRAINT speciality_pk PRIMARY KEY(speciality_id));


ALTER TABLE student ADD COLUMN speciality_id INTEGER;


ALTER TABLE student ADD CONSTRAINT student_speciality_fk
FOREIGN KEY (speciality_id) REFERENCES speciality(speciality_id) 
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;


CREATE TABLE IF NOT EXISTS course(
    course_id integer NOT NULL,
    value integer NOT NULL,
    CONSTRAINT course_pk PRIMARY KEY(course_id));

INSERT INTO course(course_id, value) VALUES (1, 1);
INSERT INTO course(course_id, value) VALUES (2, 2);
INSERT INTO course(course_id, value) VALUES (3, 3);
INSERT INTO course(course_id, value) VALUES (4, 4);
INSERT INTO course(course_id, value) VALUES (5, 5);
INSERT INTO course(course_id, value) VALUES (6, 6);


ALTER TABLE student ADD COLUMN course_id INTEGER;


ALTER TABLE student ADD CONSTRAINT student_course_fk
FOREIGN KEY (course_id) REFERENCES course(course_id) 
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;


-- Create view for descibe faculty_list_view
DROP VIEW IF EXISTS user_request_booking_hostel_view; 
CREATE VIEW user_request_booking_hostel_view AS
    SELECT
        s.full_name,
        s.user_id,
        f.name as faculty_name,
        u.university_id,
        u.short_university_name,
        r.full_name as rector_full_name,
        sp.code as speciality_code,
        sp.name as speciality_name,
        co.value as course,
        CASE 
            WHEN co.value in (1, 2, 3, 4) THEN 'B'
            ELSE 'M'
        END AS educ_level,
        CURRENT_DATE as date_today,
        CASE WHEN date_part('month', now()) >= 7 THEN date_part('year', now())::integer
            ELSE date_part('year', now() - INTERVAL '1 YEAR')::integer
        END AS start_year,
        CASE WHEN date_part('month', now()) >= 7 THEN date_part('year', now() + INTERVAL '1 YEAR')::integer
            ELSE date_part('year', now())::integer
        END AS finish_year,
        CASE WHEN LOWER(s.gender) = 'ч' THEN 'M'
            WHEN LOWER(s.gender) = 'ж' THEN 'F'
            -- if student gender isn't defined, let's say that it's male by default
            ELSE 'M'
        END AS gender
    FROM
        student s
    LEFT JOIN faculty f ON
        s.faculty_id = f.faculty_id
    LEFT JOIN university u ON
        f.university_id = u.university_id
    LEFT JOIN rector r ON
        u.rector_id = u.rector_id
    LEFT JOIN speciality sp ON
        s.speciality_id = sp.speciality_id
    LEFT JOIN course co ON
        s.course_id = co.course_id
    ORDER BY
        u.university_id,
        s.user_id;


-- Create view for display user_request_list
DROP VIEW IF EXISTS user_request_list_view;
CREATE VIEW user_request_list_view AS 
    SELECT
        ur.university_id,
        ur.user_id,
        ur.user_request_id,
        sr.service_name,
        jsonb_build_object('status_id', ur.status_id, 'status_name', st.status_name) as status,
        ur.date_created
    FROM 
        user_request ur
    LEFT JOIN status st ON
        ur.status_id = st.status_id
    LEFT JOIN service sr ON
        ur.service_id = sr.service_id
     GROUP BY
        ur.user_request_id,
        ur.user_id,
        ur.university_id,
        ur.service_id,
        st.status_name,
        sr.service_name
    ORDER BY
        ur.university_id,
        ur.user_id;


-- Create table commandant
CREATE TABLE IF NOT EXISTS commandant(
    commandant_id integer NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    telephone_number varchar(50) NOT NULL UNIQUE,
    CONSTRAINT commandant_pk PRIMARY KEY(commandant_id));

-- Insert data to table commandant
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (1, 'Ляшко Надія Михайлівна', '+380-(57)-710-78-51');
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (2, 'Любченко Володимир Віталійович', '+380-(57)-779-26-54');
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (3, 'Колосова Олена Іванівна', '+380-(57)-336-83-50');
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (4, 'Марченко Тетяна Федорівна', '+380-(57)-336-77-57');
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (5, 'Рилова Лариса Миколаївна', '+380-(57)-702-11-94');
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (6, 'Голубєва Надія Олександрівна', '+380-(57)-340-10-82');
INSERT INTO commandant(commandant_id, full_name, telephone_number) VALUES (7, 'Піпенко Світлана Миколаївна', '+380-(57)-391-02-83');

-- Create table hostel
CREATE TABLE IF NOT EXISTS hostel(
    hostel_id integer NOT NULL,
    university_id integer NOT NULL,
    number integer NOT NULL,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL,
    build VARCHAR(10) NOT NULL, 
    commandant_id integer NOT NULL,
    CONSTRAINT hostel_pk PRIMARY KEY(hostel_id));

-- link comandant_id from table hostel as FK to commandant.commandant_id
ALTER TABLE hostel ADD CONSTRAINT hostel_commandant_fk
FOREIGN KEY (commandant_id) REFERENCES commandant(commandant_id) 
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

-- link university_id from table hostel as FK to university.university_id
ALTER TABLE hostel ADD CONSTRAINT hostel_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id) 
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

-- Insert data to table hostel
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (1, 1, 1, 'Харків', 'Геліос','просп. Ювілейний', '52', 1);
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (2, 1, 2, 'Харків', 'Полюс', 'вул. Луї Пастера', '177', 2);
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (3, 1, 3, 'Харків', 'ІТ', 'вул. Цілиноградська', '40', 3);
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (4, 1, 4, 'Харків', 'Міжнародний', 'вул. Цілиноградська', '30', 4);
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (5, 1, 5, 'Харків', 'П’ятірочка', 'пров. Інженерний', '4', 5);
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (6, 1, 6, 'Харків', 'Сінергія', 'вул. Клочківська', '216а', 6);
INSERT INTO hostel(hostel_id, university_id, number, name,  city, street, build, commandant_id) VALUES (7, 1, 7, 'Харків', 'Академічний', 'вул. Ак. Філіппова', '42', 7);

-- Create view for display user_request_list
DROP VIEW IF EXISTS hostel_list_view;
CREATE VIEW hostel_list_view AS 
    SELECT
        ht.university_id,
        ht.hostel_id,
        ht.number,
        ht.name,
        ht.city,
        ht.street,
        ht.build,
        ht.commandant_id,
        co.full_name as commandant_full_name
    FROM 
        hostel ht
    LEFT JOIN commandant co ON
        co.commandant_id = ht.commandant_id
    ORDER BY
        ht.university_id,
        ht.hostel_id,
        ht.name;


ALTER TABLE student ADD COLUMN gender VARCHAR(1);
