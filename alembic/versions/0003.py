"""0003.

Revision ID: 0003
Revises: 0002
Create Date: 2023-01-08 13:32:10.734780+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sqltext="""
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
    """)


def downgrade() -> None:
    op.execute(sqltext="""
    DROP VIEW IF EXISTS user_documents_list_view;
    """)
