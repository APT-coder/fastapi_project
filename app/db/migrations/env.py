# app/db/migrations/env.py
import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

# ---- Ensure project root is on sys.path so `import app...` works ----
# env.py path: <project_root>/app/db/migrations/env.py
# project_root = three levels up from this file (.. / .. / ..)
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now safe to import application modules
try:
    from app.db.database import Base  # noqa: E402
    from app.core.config import settings  # noqa: E402
    # IMPORTANT: import modules that declare models so tables are registered on Base.metadata
    # (Add any new model modules here.)
    import app.models.user   # noqa: F401
    import app.models.category
    import app.models.product   # noqa: F401
    import app.models.role 
    import app.models.permission
    import app.models.role_permission
    import app.models.user_role
except Exception as exc:
    # helpful error to diagnose import problems when alembic runs
    raise RuntimeError(
        f"Failed to import app package. project_root={project_root!r}. "
        "Make sure you're running alembic from the project root and venv is active."
    ) from exc

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Ensure SQLAlchemy URL uses asyncpg driver if needed
async_url = settings.DATABASE_URL
if async_url.startswith("postgresql://"):
    async_url = async_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# override sqlalchemy.url from settings (so alembic CLI uses correct DB)
config.set_main_option("sqlalchemy.url", async_url)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Synchronous migration runner called inside connection.run_sync()."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' async mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
