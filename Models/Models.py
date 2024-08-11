from pydantic import BaseModel
from typing import List, Optional


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: Optional[bool] = False


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
