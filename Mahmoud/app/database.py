from sqlalchemy import (
    create_engine, Column, Integer, String, Text, ForeignKey,
    DateTime, Boolean, Float, JSON, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

engine = create_engine("sqlite:///online_exam.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()