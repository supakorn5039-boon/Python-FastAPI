from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from DB.database import Base
from services.db_services import engine
from routes.Questions import router as questions_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(questions_router)
