import asyncio
from logging.config import fileConfig

from sqlalchemy import pool, engine_from_config, text
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.database.db_url import SQLALCHEMY_DATABASE_URL


from alembic import context

# import your Base metadata
from app.database.db import Base
from app.models import user, transaction  # import all your models here

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)  # or set dynamically

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def main():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())

if __name__ == "__main__":
    main()
