"""
Database package for MediKiosk.
Provides MongoDB connection management and data access layer.
"""
from app.db.connection import mongo_connection, get_database, get_database_status
from app.db.database import (
    get_db,
    get_collection,
    db_session,
    DatabaseRepository,
    DatabaseUnavailableError,
)

__all__ = [
    "mongo_connection",
    "get_database",
    "get_database_status",
    "get_db",
    "get_collection",
    "db_session",
    "DatabaseRepository",
    "DatabaseUnavailableError",
]