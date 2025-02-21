from typing import List, Union
import pandas as pd
from beanie import PydanticObjectId
from fastapi import HTTPException
from models.recommendation import Recommendation
from models import User
from models.recommendation_hindi import RecommendationHindi
from utils import helper

admin_collection = User
user_collection = User


async def add_admin(new_admin: User) -> User:
    admin = await new_admin.create()
    return admin


async def retrieve_students() -> List[User]:
    students = await user_collection.all().to_list()
    return students


async def add_student(new_student: User) -> User:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> user_collection:
    student = await admin_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await user_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, User]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    student = await user_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False


async def add_user_query(user_id,symptoms: str):
    user_symptoms = [s.strip() for s in symptoms.split(',')]
    # Remove any extra characters, if any
    user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
    predicted_disease = helper.get_predicted_value(user_symptoms)
    
    desc, pre, med, die, wrkout = helper.helper(predicted_disease)
    user = await retrieve_student(user_id)
    my_pre = []
    for i in pre[0]:
        my_pre.append(i)
    desc_hindi = await helper.get_hindi_value(desc) or desc
    pre_hindi = await helper.trasnlate_list(my_pre)
    med_hindi = await helper.trasnlate_list(med)
    die_hindi = await helper.trasnlate_list(die)
    wrkout_hindi = await helper.trasnlate_list(wrkout)
    predicted_disease_hindi = await helper.get_hindi_value(predicted_disease) or predicted_disease
    symptoms_hindi = await helper.trasnlate_list(user_symptoms)
    data ={
        "symptoms": user_symptoms,
        "disease": predicted_disease, 
        "description":desc, 
        "precaution":my_pre, 
        "medications":med, 
        "diets":die, 
        "workouts":wrkout,
        "user": user
        }
    data_hindi ={
        "symptoms": symptoms_hindi,
        "disease": predicted_disease_hindi, 
        "description":desc_hindi, 
        "precaution":pre_hindi, 
        "medications":med_hindi, 
        "diets":die_hindi, 
        "workouts":wrkout_hindi,
        "user": user
        }
    await Recommendation(**data).save()
    await RecommendationHindi(**data_hindi).save()
    if isinstance(data.get("workouts"), pd.Series):
        data["workouts"] = data["workouts"].tolist()
    return data

async def list_user_recommendations(user_id: PydanticObjectId,page: int, size: int,lang: str):
    try:
            user_id_obj = PydanticObjectId(user_id)
            print(user_id_obj)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Query the database for recommendations belonging to the user
    recommendation_model = RecommendationHindi if lang == "hi" else Recommendation
    total_recommendations = await recommendation_model.find(recommendation_model.user.id == PydanticObjectId(user_id_obj)).count()
    recommendations = (
        await recommendation_model.find(recommendation_model.user.id == user_id_obj)
        .skip((page - 1) * size)
        .limit(size)
        .to_list()
    )
    return recommendations,total_recommendations