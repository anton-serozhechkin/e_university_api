"""0002.

Revision ID: 0002
Revises: 0001
Create Date: 2022-12-30 08:24:18.460916+00:00

"""
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sqltext="""
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
        jsonb_build_object('last_name', co.last_name, 'first_name',
         co.first_name, 'middle_name', co.middle_name)
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
    """)
    op.execute(sqltext="""
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
    """)
    op.execute(sqltext="""
    CREATE VIEW students_list_view AS
    SELECT
        st.student_id,
        json_build_object('last_name', st.last_name, 'first_name',
         st.first_name, 'middle_name', st.middle_name)
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
    """)
    op.execute(sqltext="""
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
        jsonb_agg(jsonb_build_object('id', ud.user_document_id,
         'name', ud.name,'created_at', ud.created_at)) as documents
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
    """)
    op.execute(sqltext="""
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
        json_build_object('last_name', co.last_name, 'first_name',
         co.first_name, 'middle_name', co.middle_name)
            as commandant_full_name
    FROM
        hostel ht
    LEFT JOIN commandant co ON
        co.commandant_id = ht.commandant_id
    ORDER BY
        ht.university_id,
        ht.hostel_id,
        ht.name;
    """)
    op.execute(sqltext="""
    CREATE VIEW user_request_list_view AS
    SELECT
        ur.university_id,
        ur.user_id,
        ur.user_request_id,
        sr.service_name,
        jsonb_build_object('status_id', ur.status_id, 'status_name', st.status_name)
         as status,
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
    """)
    op.execute(sqltext="""
    CREATE VIEW faculty_list_view AS
    SELECT
        f.university_id,
        f.faculty_id,
        f.name,
        f.shortname,
        f.main_email,
        f.dean_id,
        json_build_object('last_name', d.last_name, 'first_name',
         d.first_name, 'middle_name', d.middle_name)
            as dean_full_name
    FROM
        faculty f
    LEFT JOIN dean d ON
        d.dean_id = f.dean_id
    ORDER BY
        f.university_id,
        f.faculty_id,
        f.dean_id;
    """)
    op.execute(sqltext="""
    CREATE VIEW user_list_view AS
    SELECT
        u.user_id,
        u.login,
        u.last_visit_at,
        u.email,
        u.is_active,
        COALESCE(
        json_agg(json_build_object('role', u.role_id, 'role_name', r.role_name)
        ) FILTER (
        WHERE r.role_name IS NOT NULL
        ), NULL) as role,
        COALESCE(
        json_agg(json_build_object('faculty', f.faculty_id, 'faculty_name', f.name)
        ) FILTER (
        WHERE f.name IS NOT NULL
        ), NULL) as faculties,
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
    """)
    op.execute(sqltext="""
    CREATE VIEW user_request_exist_view AS
    SELECT
        ur.user_request_id,
        ur.user_id,
        ur.faculty_id,
        ur.university_id,
        ur.service_id,
        jsonb_build_object('status_id', ur.status_id, 'status_name', st.status_name)
         as status
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
        """)
    op.execute(sqltext="""
    CREATE VIEW user_request_booking_hostel_view AS
    SELECT
        json_build_object('last_name', s.last_name, 'first_name',
         s.first_name, 'middle_name', s.middle_name)
            as full_name,
        s.user_id,
        f.name as faculty_name,
        u.university_id,
        u.short_university_name,
        json_build_object('last_name', r.last_name, 'first_name',
         r.first_name, 'middle_name', r.middle_name)
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
        CASE WHEN date_part('month', now()) >= 7 THEN
         date_part('year', now() + INTERVAL '1 YEAR')::integer
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
        r.rector_id = u.rector_id
    LEFT JOIN speciality sp ON
        s.speciality_id = sp.speciality_id
    LEFT JOIN course co ON
        s.course_id = co.course_id
    ORDER BY
        u.university_id,
        s.user_id;
    """)


def downgrade() -> None:
    op.execute(sqltext="""DROP VIEW IF EXISTS hostel_accommodation_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS speciality_list_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS students_list_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS user_request_details_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS hostel_list_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS user_request_list_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS faculty_list_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS user_list_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS user_request_exist_view;""")
    op.execute(sqltext="""DROP VIEW IF EXISTS user_request_booking_hostel_view;""")
