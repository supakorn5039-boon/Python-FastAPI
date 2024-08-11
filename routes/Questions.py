from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.db_services import Get_Db
from Models.SqlModels import Questions, Choice
from Models.Models import QuestionBase
from fastapi import HTTPException
import traceback

router = APIRouter()


@router.get('/questions')
async def read_all_questions(db: Session = Depends(Get_Db)):
    try:
        result = db.query(Questions).all()
        return result
    except Exception as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/questions/{question_id}")
async def read_questions(question_id: int, db: Session = Depends(Get_Db)):
    try:
        result = db.query(Questions).filter(Questions.id == question_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/choices/{question_id}")
async def read_choices(question_id: int, db: Session = Depends(Get_Db)):
    try:
        results = db.query(Choice).filter(Choice.question_id == question_id).all()
        if not results:
            raise HTTPException(status_code=404, detail="Choices not found")
        return results
    except Exception as e:
        print(f'Error: {e}')
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/questions')
async def create_questions(question: QuestionBase, db: Session = Depends(Get_Db)):
    try:
        print(f"Received data: {question}")  # Print the received data

        db_question = Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        for choice in question.choices:
            db_choice = Choice(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
            db.add(db_choice)
        db.commit()

        return {'message': 'Question and choices created successfully'}

    except Exception as e:
        # Log the full traceback of the error
        print(f"Error occurred: {e}")
        traceback.print_exc()  # This will print the full traceback to the console
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
