from fastapi import APIRouter, Body, Request, Query
import pandas as pd

from database.database import *
from models.user import User
from schemas.recommendations import PaginatedResponse, QueryBody
from schemas.student import Response, UpdateStudentModel


router = APIRouter()

@router.post(
    "/",
    response_description="Student data added into the database",
    response_model=Response,
)
async def add_query(request: Request,body: QueryBody = Body(...)):
    user_id = request.state.user["id"]
    new_student = await add_user_query(user_id, body.query)
    
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Recommendation created successfully",
        "data": new_student,
    }

@router.get(
    "/",
    response_description="List user recommendations",
    response_model=PaginatedResponse,
)
async def get_user_recommendations(
    request: Request,
    lang: str = Query("en", description="Current Language"),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    print("Inside recommendation list")
    user_id = request.state.user["id"]
    recommendations,total = await list_user_recommendations(user_id,page,size,lang)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User recommendations fetched successfully",
        "data": recommendations,
        "total": total,
        "page": page,
        "size": size,
    }


@router.get(
    "/{recommendation_id}",
    response_description="Get a specific recommendation by ID",
    response_model=Response,
)
async def get_recommendation_by_id(
    recommendation_id: str,
    request: Request,
    lang: str = Query("en", description="Current Language"),
):
    """
    Fetch a specific recommendation by ID for the logged-in user.
    """
    print("Inside get recommendation by id")
    # Fetch user_id from request state
    user_id = request.state.user["id"]

    # Validate recommendation_id
    try:
        recommendation_id_obj = PydanticObjectId(recommendation_id)
        user_id_obj = PydanticObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Find the recommendation by ID and validate ownership
    recommendation_model = RecommendationHindi if lang == "hi" else Recommendation
    recommendation = await recommendation_model.find_one(
        {"_id": recommendation_id_obj}
    )
    print(recommendation)
    # If no recommendation is found, raise a 404 error
    if not recommendation:
        raise HTTPException(
            status_code=404, detail="Recommendation not found or access denied"
        )

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User recommendations fetched successfully",
        "data": recommendation,
    }