SET search_path to public;

CREATE TABLE IF NOT EXISTS rector(
    rector_id integer NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    middle_name varchar(50),
    CONSTRAINT rector_pk PRIMARY KEY (rector_id));

CREATE TABLE IF NOT EXISTS university (
    university_id integer NOT NULL,
    university_name varchar(255) NOT NULL,
    short_university_name varchar(50) NOT NULL,
    city varchar(255) NOT NULL,
    logo varchar(255),
    rector_id INTEGER NOT NULL,
    CONSTRAINT university_pk PRIMARY KEY (university_id));

CREATE SEQUENCE IF NOT EXISTS university_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE university ALTER COLUMN university_id SET DEFAULT nextval('university_id_seq');

ALTER TABLE university ADD CONSTRAINT university_rector_fk
FOREIGN KEY (rector_id) REFERENCES rector(rector_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS dean(
    dean_id integer NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    middle_name varchar(50),
    CONSTRAINT dean_pk PRIMARY KEY (dean_id));

CREATE SEQUENCE IF NOT EXISTS dean_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE dean ALTER COLUMN dean_id SET DEFAULT nextval('dean_id_seq');

CREATE TABLE IF NOT EXISTS faculty(
    faculty_id integer NOT NULL,
    name varchar(255) NOT NULL,
    shortname varchar(20),
    main_email varchar(50),
    university_id integer NOT NULL,
    dean_id INTEGER NOT NULL,
    CONSTRAINT faculty_pk PRIMARY KEY (faculty_id));

CREATE SEQUENCE IF NOT EXISTS faculty_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE faculty ALTER COLUMN faculty_id SET DEFAULT nextval('faculty_id_seq');

ALTER TABLE faculty ADD CONSTRAINT faculty_university_fk
FOREIGN KEY (university_id) REFERENCES university (university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE faculty ADD CONSTRAINT faculty_dean_fk
FOREIGN KEY (dean_id) REFERENCES dean(dean_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS speciality(
    speciality_id integer NOT NULL,
    faculty_id integer NOT NULL,
    code integer NOT NULL,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT speciality_pk PRIMARY KEY(speciality_id));

ALTER TABLE speciality ADD CONSTRAINT speciality_faculty_fk 
FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS course(
    course_id integer NOT NULL,
    value integer NOT NULL,
    CONSTRAINT course_pk PRIMARY KEY(course_id));

CREATE TABLE IF NOT EXISTS student (
    student_id integer NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    middle_name varchar(50),
    telephone_number varchar(50) NOT NULL UNIQUE,
    faculty_id integer NOT NULL,
    user_id integer,
    speciality_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    gender VARCHAR(1) NOT NULL,
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT student_pk PRIMARY KEY(student_id));

CREATE SEQUENCE IF NOT EXISTS student_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE student ALTER COLUMN student_id SET DEFAULT nextval('student_id_seq');

ALTER TABLE student ADD CONSTRAINT student_faculty_fk
FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE student ADD CONSTRAINT student_speciality_fk
FOREIGN KEY (speciality_id) REFERENCES speciality(speciality_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE student ADD CONSTRAINT student_course_fk
FOREIGN KEY (course_id) REFERENCES course(course_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS "user"(
    user_id integer NOT NULL,
    login varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    last_visit_at timestamp with time zone default (now() at time zone 'utc'),
    email varchar(100) NOT NULL,
    role_id integer NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    UNIQUE (login, email),
    CONSTRAINT user_pk PRIMARY KEY(user_id));

CREATE SEQUENCE IF NOT EXISTS user_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE "user" ALTER COLUMN user_id SET DEFAULT nextval('user_id_seq');

ALTER TABLE student ADD CONSTRAINT student_user_fk
FOREIGN KEY (user_id) REFERENCES "user"(user_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS role(
    role_id integer NOT NULL,
    role_name varchar(50) NOT NULL,
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT role_pk PRIMARY KEY(role_id));

CREATE SEQUENCE IF NOT EXISTS role_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE role ALTER COLUMN role_id SET DEFAULT nextval('role_id_seq');

ALTER TABLE "user" ADD CONSTRAINT user_role_fk
FOREIGN KEY(role_id) REFERENCES role(role_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS action(
    role_id integer NOT NULL,
    action_name varchar(50) NOT NULL,
    action_id integer NOT NULL,
    CONSTRAINT action_pk PRIMARY KEY(action_id));

CREATE SEQUENCE IF NOT EXISTS action_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE action ALTER COLUMN action_id SET DEFAULT nextval('action_id_seq');

ALTER TABLE action ADD CONSTRAINT action_role_fk
FOREIGN KEY(role_id) REFERENCES role(role_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS user_faculty(
    user_id integer NOT NULL,
    faculty_id integer NOT NULL,
    CONSTRAINT user_faculty_pk PRIMARY KEY(user_id, faculty_id));

ALTER TABLE user_faculty ADD CONSTRAINT user_faculty_user_fk
FOREIGN KEY(user_id) REFERENCES "user"(user_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE user_faculty ADD CONSTRAINT user_faculty_faculty_fk
FOREIGN KEY(faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS one_time_token(
    student_id integer NOT NULL,
    token_id integer NOT NULL,
    token varchar(255) NOT NULL,
    expires_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT one_time_token_pk PRIMARY KEY (token_id));

CREATE SEQUENCE IF NOT EXISTS token_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE one_time_token ALTER COLUMN token_id SET DEFAULT nextval('token_id_seq');

ALTER TABLE one_time_token ADD CONSTRAINT one_time_token_student_fk
FOREIGN KEY (student_id) REFERENCES student(student_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS service(
    service_id integer NOT NULL,
    service_name varchar(255) NOT NULL,
    CONSTRAINT service_pk PRIMARY KEY (service_id));

CREATE TABLE IF NOT EXISTS status(
    status_id integer NOT NULL,
    status_name varchar(50) NOT NULL,
    CONSTRAINT status_pk PRIMARY KEY (status_id));

CREATE TABLE IF NOT EXISTS user_request(
    user_request_id integer NOT NULL,
    faculty_id integer NOT NULL,
    university_id integer NOT NULL,
    user_id integer NOT NULL,
    service_id integer NOT NULL,
    status_id integer NOT NULL,
    comment VARCHAR(255),
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT user_request_pk PRIMARY KEY(user_request_id));

CREATE SEQUENCE IF NOT EXISTS user_request_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE user_request ALTER COLUMN user_request_id SET DEFAULT nextval('user_request_id_seq');

ALTER TABLE user_request ADD CONSTRAINT user_request_service_fk
FOREIGN KEY (service_id) REFERENCES service(service_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE user_request ADD CONSTRAINT user_request_status_fk
FOREIGN KEY (status_id) REFERENCES status(status_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE user_request ADD CONSTRAINT user_request_faculty_fk
FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE user_request ADD CONSTRAINT user_request_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE user_request ADD CONSTRAINT user_request_user_fk
FOREIGN KEY (user_id) REFERENCES "user"(user_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS user_document(
    user_document_id integer NOT NULL,
    name varchar(255) NOT NULL,
    content varchar(255) NOT NULL,
    user_request_id integer NOT NULL,
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT user_document_pk PRIMARY KEY (user_document_id));

CREATE SEQUENCE IF NOT EXISTS user_document_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE user_document ALTER COLUMN user_document_id SET DEFAULT nextval('user_document_id_seq');

CREATE TABLE IF NOT EXISTS bed_place(
    bed_place_id integer NOT NULL,
    bed_place_name varchar(50) NOT NULL,
    CONSTRAINT bed_place_pk PRIMARY KEY (bed_place_id));

CREATE TABLE IF NOT EXISTS commandant(
    commandant_id integer NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    telephone_number varchar(50) NOT NULL UNIQUE,
    CONSTRAINT commandant_pk PRIMARY KEY(commandant_id));

CREATE TABLE IF NOT EXISTS hostel(
    hostel_id integer NOT NULL,
    university_id integer NOT NULL,
    number integer NOT NULL,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL,
    build VARCHAR(10) NOT NULL,
    commandant_id integer NOT NULL,
    month_price decimal(6, 2) NOT NULL,
    instagram VARCHAR(255),
    telegram VARCHAR(255),
    CONSTRAINT hostel_pk PRIMARY KEY(hostel_id));

ALTER TABLE hostel ADD CONSTRAINT hostel_commandant_fk
FOREIGN KEY (commandant_id) REFERENCES commandant(commandant_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE hostel ADD CONSTRAINT hostel_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS user_request_review(
    user_request_review_id integer NOT NULL,
    university_id integer NOT NULL,
    user_request_id integer NOT NULL,
    reviewer integer NOT NULL,
    hostel_id integer,
    room_number integer,
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    start_accommodation_date date,
    end_accommodation_date date,
    total_sum decimal(7, 2),
    payment_deadline_date date,
    remark varchar(255),
    bed_place_id integer,
    CONSTRAINT user_req_rew_pk PRIMARY KEY(user_request_review_id));

CREATE SEQUENCE IF NOT EXISTS user_request_review_id_seq AS bigint START WITH 1 INCREMENT BY 1;

ALTER TABLE user_request_review ALTER COLUMN user_request_review_id SET DEFAULT nextval('user_request_review_id_seq');

ALTER TABLE user_request_review ADD CONSTRAINT user_request_review_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE user_request_review ADD CONSTRAINT user_request_review_user_request_fk
FOREIGN KEY (user_request_id) REFERENCES user_request(user_request_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE user_request_review ADD CONSTRAINT user_request_review_user_fk
FOREIGN KEY (reviewer) REFERENCES "user"(user_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE user_request_review ADD CONSTRAINT user_request_review_hostel_fk
FOREIGN KEY (hostel_id) REFERENCES hostel(hostel_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE user_request_review ADD CONSTRAINT user_request_review_bed_place_fk
FOREIGN KEY (bed_place_id) REFERENCES bed_place(bed_place_id)
MATCH FULL ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS requisites(
    requisites_id integer NOT NULL,
    iban VARCHAR(100),
    university_id integer NOT NULL,
    organisation_code VARCHAR(50),
    service_id integer NOT NULL,
    payment_recognition VARCHAR(255),
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT requisites_pk PRIMARY KEY(requisites_id));

ALTER TABLE requisites ADD CONSTRAINT requisites_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE requisites ADD CONSTRAINT requisites_service_fk
FOREIGN KEY (service_id) REFERENCES service(service_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS service_document(
    service_document_id integer NOT NULL,
    service_id INTEGER NOT NULL,
    university_id INTEGER NOT NULL,
    documents JSON NOT NULL,
    created_at timestamp with time zone default (now() at time zone 'utc'),
    updated_at timestamp with time zone default (now() at time zone 'utc'),
    CONSTRAINT service_document_pk PRIMARY KEY(service_document_id));

ALTER TABLE service_document ADD CONSTRAINT service_document_service_fk
FOREIGN KEY (service_id) REFERENCES service(service_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE service_document ADD CONSTRAINT service_document_university_fk
FOREIGN KEY (university_id) REFERENCES university(university_id)
MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE;

DROP VIEW IF EXISTS hostel_accommodation_view;
CREATE VIEW hostel_accommodation_view AS
    SELECT
        urr.user_request_review_id,
        urr.university_id,
        urr.user_request_id,
        urr.room_number,
        urr.start_accommodation_date,
        urr.end_accommodation_date,
        ht.month_price,
        jsonb_build_object('name', ht.name, 'number', ht.number)
            as hostel_name,
        jsonb_build_object('city', ht.city, 'street', ht.street, 'build', ht.build)
            as hostel_address,
        bd.bed_place_name,
        urr.total_sum,
        re.iban,
        un.university_name,
        re.organisation_code,
        re.payment_recognition,
        jsonb_build_object('last_name', co.last_name, 'first_name', co.first_name, 'middle_name', co.middle_name) 
            as commandant_full_name,
        co.telephone_number,
        sd.documents
    FROM
        user_request_review urr
    LEFT JOIN hostel ht ON
        ht.hostel_id = urr.hostel_id
    LEFT JOIN bed_place bd ON
        bd.bed_place_id = urr.bed_place_id
    LEFT JOIN user_request ur ON
        ur.user_request_id = urr.user_request_id
    LEFT JOIN service se ON
        se.service_id = ur.service_id
    LEFT JOIN requisites re ON
        re.service_id = re.service_id AND
        re.university_id = urr.university_id
    LEFT JOIN university un ON
        un.university_id = urr.university_id
    LEFT JOIN commandant co ON
        co.commandant_id = ht.commandant_id
    LEFT JOIN service_document sd ON
        sd.service_id = se.service_id AND
        sd.university_id = urr.university_id;

DROP VIEW IF EXISTS speciality_list_view;
CREATE VIEW speciality_list_view AS
    SELECT
    s.faculty_id,
    s.speciality_id,
    f.university_id,
    json_build_object('code', s.code, 'full_name', s.name) as speciality_info
    FROM
        speciality s
    LEFT JOIN faculty f ON
        f.faculty_id = s.faculty_id
    ORDER BY s.code, s.name;

DROP VIEW IF EXISTS students_list_view;
CREATE VIEW students_list_view AS
    SELECT
        st.student_id,
        json_build_object('last_name', st.last_name, 'first_name', st.first_name, 'middle_name', st.middle_name)
            as student_full_name,
        st.telephone_number,
        st.user_id,
	    f.university_id,
        st.faculty_id,
        st.speciality_id,
        st.course_id,
        st.gender
    FROM
        student st
    LEFT JOIN faculty f ON
        st.faculty_id = f.faculty_id
    ORDER BY
        f.university_id,
        st.faculty_id,
        st.last_name,
        st.first_name,
        st.middle_name;

DROP VIEW IF EXISTS user_request_details_view;
CREATE VIEW user_request_details_view AS
    SELECT
        ur.user_request_id,
        ur.university_id,
        ur.created_at,
        sr.service_name,
        st.status_name,
        ur.status_id,
        ur.comment,
        jsonb_build_object('name', ht.name, 'number', ht.number) as hostel_name,
        urr.room_number,
        bd.bed_place_name,
        urr.remark,
        jsonb_agg(jsonb_build_object('id', ud.user_document_id, 'name', ud.name,'created_at', ud.created_at)) as documents
    FROM
        user_request ur
    LEFT JOIN user_request_review urr ON
        ur.user_request_id = urr.user_request_id
    LEFT JOIN status st ON
        ur.status_id = st.status_id
	LEFT JOIN service sr ON
		ur.service_id = sr.service_id
	LEFT JOIN hostel ht ON
		ht.hostel_id = urr.hostel_id
	LEFT JOIN bed_place bd ON
		bd.bed_place_id = urr.bed_place_id
    LEFT JOIN user_document ud ON
		ud.user_request_id = ur.user_request_id
	GROUP BY
		ur.user_request_id,
        ur.university_id,
        ur.created_at,
        sr.service_name,
        st.status_name,
        ur.status_id,
        ur.comment,
		ht.name,
		ht.number,
        urr.room_number,
        bd.bed_place_name,
        urr.remark
    ORDER BY
        ur.university_id,
        ur.user_request_id;

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
        json_build_object('last_name', co.last_name, 'first_name', co.first_name, 'middle_name', co.middle_name)
            as commandant_full_name
    FROM
        hostel ht
    LEFT JOIN commandant co ON
        co.commandant_id = ht.commandant_id
    ORDER BY
        ht.university_id,
        ht.hostel_id,
        ht.name;

DROP VIEW IF EXISTS user_request_list_view;
CREATE VIEW user_request_list_view AS
    SELECT
        ur.university_id,
        ur.user_id,
        ur.user_request_id,
        sr.service_name,
        jsonb_build_object('status_id', ur.status_id, 'status_name', st.status_name) as status,
        ur.created_at
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

DROP VIEW IF EXISTS faculty_list_view;
CREATE VIEW faculty_list_view AS
    SELECT
        f.university_id,
        f.faculty_id,
        f.name,
        f.shortname,
        f.main_email,
        f.dean_id,
        json_build_object('last_name', d.last_name, 'first_name', d.first_name, 'middle_name', d.middle_name)
            as dean_full_name
    FROM
        faculty f
    LEFT JOIN dean d ON
        d.dean_id = f.dean_id
    ORDER BY
        f.university_id,
        f.faculty_id,
        f.dean_id;

DROP VIEW IF EXISTS user_list_view;
CREATE VIEW user_list_view AS
    SELECT
        u.user_id,
        u.login,
        u.last_visit_at,
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
        u.last_visit_at,
        u.email,
        u.is_active,
        un.university_id
    ORDER BY
        un.university_id,
        u.user_id,
        u.is_active;

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

DROP VIEW IF EXISTS user_request_booking_hostel_view;
CREATE VIEW user_request_booking_hostel_view AS
    SELECT
        json_build_object('last_name', s.last_name, 'first_name', s.first_name, 'middle_name', s.middle_name)
            as full_name,
        s.user_id,
        f.name as faculty_name,
        u.university_id,
        u.short_university_name,
        json_build_object('last_name', r.last_name, 'first_name', r.first_name, 'middle_name', r.middle_name)
            as rector_full_name,
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


DROP VIEW IF EXISTS user_documents_list_view;
CREATE VIEW user_documents_list_view AS
    SELECT
        ur.university_id,
        ud.user_document_id,
        ur.user_id,
        ud.name,
        ud.created_at,
        ud.updated_at
    FROM
        user_document ud
    LEFT JOIN user_request ur ON
        ur.user_request_id = ud.user_request_id
    WHERE
        ur.status_id in (1, 3)
    ORDER BY
        ur.university_id,
        ud.user_document_id,
        ur.user_id;

DROP VIEW IF EXISTS user_request_hostel_warrant_view;
CREATE VIEW user_request_hostel_warrant_view AS
    SELECT
    urr.user_request_review_id,
    urr.room_number as room_number,
    urr.created_at as created_at,
    urr.service_id as service_id,
    h.number as hostel_number,
    h.street as hostel_street,
    h.build as hostel_build,
    bp.bed_place_name as bed_place_name,
    u.university_name as university_name,
    u.logo as university_logo,
    u.city as university_city,
    ur.status_id as status_id,
    json_build_object('last_name', s.last_name, 'first_name', s.first_name, 'middle_name', s.middle_name)
            as student_full_name,
    s.gender as student_gender,
    f.shortname as faculty_shortname,
    json_build_object('last_name', d.last_name, 'first_name', d.first_name, 'middle_name', d.middle_name)
        as dean_full_name,
    FROM
        user_request_review urr
    LEFT JOIN hostel h ON
        urr.hostel_id = h.hostel_id
    LEFT JOIN bed_place bp ON
        urr.bed_place_id = bp.bed_place_id
    LEFT JOIN university u ON
        urr.university_id = u.university_id
    LEFT JOIN user_request ur ON
        urr.user_request_id = ur.user_request_id
    LEFT JOIN "user" user ON
        ur.user_id = user.user_id
    LEFT JOIN student s ON
        user.student = s.user_id
    LEFT JOIN faculty f ON
        ur.faculty_id = f.faculty_id
    LEFT JOIN dean d ON
        f.dean_id = d.dean_id
