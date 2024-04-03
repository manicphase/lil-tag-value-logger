from sqlite3 import Timestamp
from sqlalchemy import Column, Integer, Boolean, String, DateTime, Float
from db.database import Base

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True)
    recording_id = Column(String, index=True)
    tag = Column(String, index=True)
    value = Column(Integer)
    timestamp = Column(DateTime, index=True)

class GraphingSession(Base):
    __tablename__ = "graphing_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    data = Column(String)