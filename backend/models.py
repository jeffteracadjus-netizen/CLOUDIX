from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    companies = relationship(
        "Company",
        back_populates="user"
    )


class Company(Base):
    __tablename__ = "companies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    sector = Column(
        String,
        nullable=True
    )

    size = Column(
        String,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    goal = Column(
        Text,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="companies"
    )

    financial_files = relationship(
        "FinancialFile",
        back_populates="company"
    )


class FinancialFile(Base):
    __tablename__ = "financial_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    company = relationship(
        "Company",
        back_populates="financial_files"
    )