"""0004 version migration.

Revision ID: 0004
Revises: 0004
Create Date: 2023-01-18 21:24:28.874997+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sqltext="""
        CREATE VIEW user_request_hostel_accommodation_warrant_view AS
    SELECT
        urr.user_request_review_id,
        urr.room_number,
        urr.user_request_id,
        urr.created_at,
        h.number as hostel_number,
        h.street as hostel_street,
        h.build as hostel_build,
        bp.bed_place_name,
        u.university_name,
        u.short_university_name,
        u.city as university_city,
        ur.status_id,
        ur.user_id,
        json_build_object('last_name', s.last_name, 'first_name', s.first_name, 'middle_name', s.middle_name)
                as student_full_name,
        s.gender as student_gender,
        f.shortname as faculty_shortname,
        json_build_object('last_name', d.last_name, 'first_name', d.first_name, 'middle_name', d.middle_name)
            as dean_full_name
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
    LEFT JOIN student s ON
        ur.user_id = s.user_id
    LEFT JOIN faculty f ON
        ur.faculty_id = f.faculty_id
    LEFT JOIN dean d ON
        f.dean_id = d.dean_id
    ORDER BY
        urr.user_request_review_id,
        urr.user_request_id,
        urr.created_at;
        """)


def downgrade() -> None:
    op.execute(sqltext="""
    DROP VIEW IF EXISTS user_request_hostel_accommodation_warrant_view;
    """)
