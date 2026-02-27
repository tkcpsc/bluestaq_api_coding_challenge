from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

"""
Database configuration for the Notes API.

This module initializes the SQLAlchemy engine and session factory used
throughout the application. It also defines the Base class that all
database models inherit from.
"""

# SQLite database file stored in the project root directory
DATABASE_URL = "sqlite:///./notes.db"


# Create the SQLAlchemy engine which manages database connections
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite when used with multiple threads
)


# Session factory used to create database sessions for requests
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Any database model should inherit from this class so SQLAlchemy
    can track table definitions and generate the schema.
    """
    pass