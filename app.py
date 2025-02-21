from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.recommendation import router as RecommendationRouter
from routes.student import router as StudentRouter

app = FastAPI()

token_listener = JWTBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Remove wildcard (*)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Restrict methods
    allow_headers=["Authorization", "Content-Type"],  # Specify allowed headers
)

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/auth")
app.include_router(RecommendationRouter, tags=["Recommendations"], prefix="/recommendations",dependencies=[Depends(token_listener)])
app.include_router(StudentRouter,tags=["Students"],prefix="/student",dependencies=[Depends(token_listener)])
