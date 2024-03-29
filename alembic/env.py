import pathlib
from logging.config import fileConfig

from alembic import context
from sqlalchemy_utils import create_database, database_exists

from apps.authorization.models import Base as AuthBase
from apps.common.db import Base, engine
from apps.educational_institutions.models import Base as EduBase
from apps.hostel.models import Base as HostelBase
from apps.services.models import Base as ServiceBase
from apps.users.models import Base as UserBase
from settings import Settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

if not database_exists(Settings.POSTGRES_DSN):
    create_database(Settings.POSTGRES_DSN)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    MIGRATIONS_DIR = pathlib.Path(__file__).parent.resolve()
    SQL_VERSIONS_DIR = MIGRATIONS_DIR / "sql_versions"
    if not SQL_VERSIONS_DIR.exists():
        SQL_VERSIONS_DIR.mkdir()

    context.configure(
        url=Settings.POSTGRES_DSN,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        transactional_ddl=False,
        output_buffer=open(
            SQL_VERSIONS_DIR / f"{context.get_head_revision()}.sql", "w"
        ),
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
