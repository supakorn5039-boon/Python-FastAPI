from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from DB.database import Base


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    choices = relationship("Choice", back_populates="question")


class Choice(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Integer)
    question_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship("Questions", back_populates="choices")
