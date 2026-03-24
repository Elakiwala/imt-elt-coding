"""
Database connection manager for KICKZ EMPIRE ELT pipeline.
Uses SQLAlchemy to connect to AWS RDS PostgreSQL.

TP1 — Step 0: Configure the database connection.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration from .env
# ---------------------------------------------------------------------------
RDS_HOST = os.getenv("RDS_HOST")
RDS_PORT = os.getenv("RDS_PORT", "5432")
RDS_DATABASE = os.getenv("RDS_DATABASE")
RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")

BRONZE_SCHEMA = os.getenv("BRONZE_SCHEMA", "bronze_group5")
SILVER_SCHEMA = os.getenv("SILVER_SCHEMA", "silver_group5")
GOLD_SCHEMA = os.getenv("GOLD_SCHEMA", "gold_group5")


def get_engine():
    """
    Create and return a SQLAlchemy engine connected to PostgreSQL (AWS RDS).

    Returns:
        sqlalchemy.Engine: The connection engine.

    SQLAlchemy URL example:
        postgresql://user:password@host:port/database

    Docs:
        https://docs.sqlalchemy.org/en/20/core/engines.html
    """
    # TODO: Build the PostgreSQL connection URL and create the engine
    # Hint: use create_engine() from SQLAlchemy
    # The URL must follow this format: postgresql://{user}:{password}@{host}:{port}/{database}
    user = os.getenv("RDS_USER")
    password = os.getenv("RDS_PASSWORD")
    host = os.getenv("RDS_HOST")
    port = os.getenv("RDS_PORT", "5432")
    database = os.getenv("RDS_DATABASE")

    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(url)
    return engine

    
    #raise NotImplementedError("TODO: Implement get_engine()")


def test_connection():
    """
    Test the database connection.
    Executes a simple query (SELECT 1) and prints the result.

    Returns:
        bool: True if the connection succeeds, False otherwise.
    """
    # TODO: Use get_engine() to connect and execute SELECT 1
    # Hint: use engine.connect() inside a with block
    #       then connection.execute(text("SELECT 1"))
    try:
        engine = get_engine()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(result.scalar())
        return True

    except Exception as e:
        print("Connection failed:", e)
        return False
    
    #raise NotImplementedError("TODO: Implement test_connection()")


def execute_sql(sql: str, params: dict = None):
    """
    Execute an arbitrary SQL query.

    Args:
        sql (str): The SQL query to execute.
        params (dict, optional): Query parameters.

    Returns:
        The query result (for SELECT), None for other statements.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        conn.commit()
        return result


# ---------------------------------------------------------------------------
# Entry point to test the connection
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🔌 Testing connection to PostgreSQL (AWS RDS)...")
    if test_connection():
        print(f"✅ Connected successfully!")
        print(f"   Schemas: {BRONZE_SCHEMA}, {SILVER_SCHEMA}, {GOLD_SCHEMA}")
    else:
        print("❌ Connection failed. Check your .env file")
