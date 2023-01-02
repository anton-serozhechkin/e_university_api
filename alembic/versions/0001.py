"""0001

Revision ID: 0001
Revises: 
Create Date: 2022-12-29 17:58:25.740737+00:00

"""
import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bed_place",
        sa.Column("bed_place_id", sa.INTEGER(), nullable=False),
        sa.Column("bed_place_name", sa.VARCHAR(length=50), nullable=False),
        sa.PrimaryKeyConstraint("bed_place_id", name=op.f("bed_place_pk")),
    )
    op.create_table(
        "commandant",
        sa.Column("commandant_id", sa.INTEGER(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("middle_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("telephone_number", sa.VARCHAR(length=50), nullable=False),
        sa.PrimaryKeyConstraint("commandant_id", name=op.f("commandant_pk")),
        sa.UniqueConstraint("telephone_number", name=op.f("commandant_telephone_number_key")),
    )
    op.create_table(
        "course",
        sa.Column("course_id", sa.INTEGER(), nullable=False),
        sa.Column("value", sa.INTEGER(), nullable=False),
        sa.PrimaryKeyConstraint("course_id", name=op.f("course_pk")),
    )
    op.create_table(
        "dean",
        sa.Column("dean_id", sa.INTEGER(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("middle_name", sa.VARCHAR(length=50), nullable=True),
        sa.PrimaryKeyConstraint("dean_id", name=op.f("dean_pk")),
    )
    op.create_table(
        "rector",
        sa.Column("rector_id", sa.INTEGER(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("middle_name", sa.VARCHAR(length=50), nullable=True),
        sa.PrimaryKeyConstraint("rector_id", name=op.f("rector_pk")),
    )
    op.create_table(
        "role",
        sa.Column("role_id", sa.INTEGER(), nullable=False),
        sa.Column("role_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("role_id", name=op.f("role_pk")),
    )
    op.create_table(
        "service",
        sa.Column("service_id", sa.INTEGER(), nullable=False),
        sa.Column("service_name", sa.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint("service_id", name=op.f("service_pk")),
    )
    op.create_table(
        "status",
        sa.Column("status_id", sa.INTEGER(), nullable=False),
        sa.Column("status_name", sa.VARCHAR(length=50), nullable=False),
        sa.PrimaryKeyConstraint("status_id", name=op.f("status_pk")),
    )
    op.create_table(
        "action",
        sa.Column("action_id", sa.INTEGER(), nullable=False),
        sa.Column("action_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("role_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ("role_id",),
            ["role.role_id"],
            name=op.f("action_role_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("action_id", name=op.f("action_pk")),
    )
    op.create_table(
        "university",
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.Column("university_name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("short_university_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("logo", sa.VARCHAR(length=255), nullable=True),
        sa.Column("rector_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ("rector_id",),
            ["rector.rector_id"],
            name=op.f("university_rector_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("university_id", name=op.f("university_pk")),
    )
    op.create_table(
        "user",
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.Column("login", sa.VARCHAR(length=50), nullable=False),
        sa.Column("password", sa.VARCHAR(length=255), nullable=False),
        sa.Column(
            "last_visit_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("email", sa.VARCHAR(length=100), nullable=False),
        sa.Column("is_active", sa.BOOLEAN(), nullable=True),
        sa.Column("role_id", sa.INTEGER(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ("role_id",),
            ["role.role_id"],
            name=op.f("user_role_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("user_pk")),
        sa.UniqueConstraint("email", name=op.f("user_email_key")),
        sa.UniqueConstraint("login", name=op.f("user_login_key")),
    )
    op.create_table(
        "faculty",
        sa.Column("faculty_id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("shortname", sa.VARCHAR(length=20), nullable=True),
        sa.Column("main_email", sa.VARCHAR(length=50), nullable=True),
        sa.Column("dean_id", sa.INTEGER(), nullable=True),
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ("dean_id",),
            ["dean.dean_id"],
            name=op.f("faculty_dean_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("university_id",),
            ["university.university_id"],
            name=op.f("faculty_university_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("faculty_id", name=op.f("faculty_pk")),
    )
    op.create_table(
        "hostel",
        sa.Column("hostel_id", sa.INTEGER(), nullable=False),
        sa.Column("number", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=100), nullable=False),
        sa.Column("city", sa.VARCHAR(length=100), nullable=False),
        sa.Column("street", sa.VARCHAR(length=100), nullable=False),
        sa.Column("build", sa.VARCHAR(length=10), nullable=False),
        sa.Column("month_price", sa.DECIMAL(precision=6, scale=2), nullable=False),
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.Column("commandant_id", sa.INTEGER(), nullable=False),
        sa.Column("instagram", sa.VARCHAR(255), nullable=True),
        sa.Column("telegram", sa.VARCHAR(255), nullable=True),
        sa.ForeignKeyConstraint(
            ("commandant_id",),
            ["commandant.commandant_id"],
            name=op.f("hostel_commandant_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("university_id",),
            ["university.university_id"],
            name=op.f("hostel_university_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("hostel_id", name=op.f("hostel_pk")),
    )
    op.create_table(
        "requisites",
        sa.Column("requisites_id", sa.INTEGER(), nullable=False),
        sa.Column("iban", sa.VARCHAR(length=100), nullable=True),
        sa.Column("organisation_code", sa.VARCHAR(length=50), nullable=True),
        sa.Column("payment_recognition", sa.VARCHAR(length=255), nullable=True),
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.Column("service_id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ("service_id",),
            ["service.service_id"],
            name=op.f("requisites_service_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("university_id",),
            ["university.university_id"],
            name=op.f("requisites_university_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("requisites_id", name=op.f("requisites_pk")),
    )
    op.create_table(
        "speciality",
        sa.Column("speciality_id", sa.INTEGER(), nullable=False),
        sa.Column("code", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("faculty_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ("faculty_id",),
            ["faculty.faculty_id"],
            name=op.f("speciality_faculty_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("speciality_id", name=op.f("speciality_pk")),
    )
    op.create_table(
        "user_faculty",
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.Column("faculty_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ("faculty_id",),
            ["faculty.faculty_id"],
            name=op.f("user_faculty_faculty_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("user_id",),
            ["user.user_id"],
            name=op.f("user_faculty_user_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", "faculty_id", name=op.f("user_faculty_pk")),
    )
    op.create_table(
        "user_request",
        sa.Column("user_request_id", sa.INTEGER(), nullable=False),
        sa.Column("comment", sa.VARCHAR(length=255), nullable=True),
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.Column("service_id", sa.INTEGER(), nullable=False),
        sa.Column("faculty_id", sa.INTEGER(), nullable=False),
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.Column("status_id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ("faculty_id",),
            ["faculty.faculty_id"],
            name=op.f("user_request_faculty_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("service_id",),
            ["service.service_id"],
            name=op.f("user_request_service_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("status_id",),
            ["status.status_id"],
            name=op.f("user_request_status_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("university_id",),
            ["university.university_id"],
            name=op.f("user_request_university_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("user_id",),
            ["user.user_id"],
            name=op.f("user_request_user_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_request_id", name=op.f("user_request_pk")),
    )
    op.create_table(
        "student",
        sa.Column("student_id", sa.INTEGER(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=False),
        sa.Column("middle_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("telephone_number", sa.VARCHAR(length=50), nullable=False),
        sa.Column("gender", sa.VARCHAR(length=1), nullable=False),
        sa.Column("course_id", sa.INTEGER(), nullable=False),
        sa.Column("speciality_id", sa.INTEGER(), nullable=False),
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("faculty_id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ("course_id",),
            ["course.course_id"],
            name=op.f("student_course_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("faculty_id",),
            ["faculty.faculty_id"],
            name=op.f("student_faculty_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("speciality_id",),
            ["speciality.speciality_id"],
            name=op.f("student_speciality_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("user_id",),
            ["user.user_id"],
            name=op.f("student_user_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("student_id", name=op.f("student_pk")),
        sa.UniqueConstraint("telephone_number", name=op.f("student_telephone_number_key")),
    )
    op.create_table(
        "user_document",
        sa.Column("user_document_id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("content", sa.VARCHAR(length=255), nullable=False),
        sa.Column("user_request_id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ("user_request_id",),
            ["user_request.user_request_id"],
            name=op.f("user_document_user_request_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_document_id", name=op.f("user_document_pk")),
    )
    op.create_table(
        "user_request_review",
        sa.Column("user_request_review_id", sa.INTEGER(), nullable=False),
        sa.Column("room_number", sa.INTEGER(), nullable=True),
        sa.Column("start_accommodation_date", sa.DATE(), nullable=True),
        sa.Column("end_accommodation_date", sa.DATE(), nullable=True),
        sa.Column("total_sum", sa.DECIMAL(precision=7, scale=2), nullable=True),
        sa.Column("payment_deadline_date", sa.DATE(), nullable=True),
        sa.Column("remark", sa.VARCHAR(length=255), nullable=True),
        sa.Column("bed_place_id", sa.INTEGER(), nullable=True),
        sa.Column("reviewer", sa.INTEGER(), nullable=False),
        sa.Column("hostel_id", sa.INTEGER(), nullable=True),
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.Column("user_request_id", sa.INTEGER(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(
            ("bed_place_id",),
            ["bed_place.bed_place_id"],
            name=op.f("user_request_review_bed_place_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("hostel_id",),
            ["hostel.hostel_id"],
            name=op.f("user_request_review_hostel_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("reviewer",),
            ["user.user_id"],
            name=op.f("user_request_review_reviewer_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("university_id",),
            ["university.university_id"],
            name=op.f("user_request_review_university_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("user_request_id",),
            ["user_request.user_request_id"],
            name=op.f("user_request_review_user_request_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_request_review_id", name=op.f("user_request_review_pk")),
    )
    op.create_table(
        "one_time_token",
        sa.Column("token_id", sa.INTEGER(), nullable=False),
        sa.Column("token", sa.VARCHAR(length=255), nullable=False),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("student_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ("student_id",),
            ["student.student_id"],
            name=op.f("one_time_token_student_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("token_id", name=op.f("one_time_token_pk")),
    )
    op.create_table(
        "service_document",
        sa.Column("service_document_id", sa.INTEGER(), nullable=False),
        sa.Column("service_id", sa.INTEGER(), nullable=False),
        sa.Column("university_id", sa.INTEGER(), nullable=False),
        sa.Column("documents", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(
            ("university_id",),
            ["university.university_id"],
            name=op.f("service_document_university_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ("service_id",),
            ["service.service_id"],
            name=op.f("service_document_service_fk"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("service_document_id", name=op.f("service_document_pk")),
    )


def downgrade() -> None:
    op.drop_table("one_time_token")
    op.drop_table("user_request_review")
    op.drop_table("user_document")
    op.drop_table("student")
    op.drop_table("user_request")
    op.drop_table("user_faculty")
    op.drop_table("speciality")
    op.drop_table("requisites")
    op.drop_table("hostel")
    op.drop_table("faculty")
    op.drop_table("user")
    op.drop_table("service_document")
    op.drop_table("university")
    op.drop_table("action")
    op.drop_table("status")
    op.drop_table("service")
    op.drop_table("role")
    op.drop_table("rector")
    op.drop_table("dean")
    op.drop_table("course")
    op.drop_table("commandant")
    op.drop_table("bed_place")
