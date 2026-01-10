from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)  
    description = Column(Text, nullable=True)
    email = Column(String, nullable=False, index=True)
