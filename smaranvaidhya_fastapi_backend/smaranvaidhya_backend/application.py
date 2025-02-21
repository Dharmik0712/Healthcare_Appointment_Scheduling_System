from fastapi import FastAPI,HTTPException,Response,Request,UploadFile, File ,Query
import json
import smaranvaidhya_db as smv_db
from typing import Dict
from fastapi.responses import JSONResponse,StreamingResponse
import schemas
import base64
import psycopg2
from io import BytesIO
from psycopg2 import sql
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #"http://localhost:6078" | Change "*" to specific origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/fastapi")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/attempt_to_login_for_user")
def attempt_to_login_for_user(login_data: schemas.LoginForUser):
    valid_user, user_id = smv_db.validate_login_details(login_data.dict())

    if valid_user:
        return JSONResponse(content={"status": "Login Successful", "user_id": user_id}, status_code=200)
    else:
        return JSONResponse(content={"status": "Login Failed"}, status_code=401)  # No user_id in failure case


@app.post("/save_user_registration_details")
def save_user_registration_details(reg_details:schemas.UserRegistration):
    print(reg_details)
    result = smv_db.save_user_registration_details(reg_details.dict())
    response = {
        "data" : result
    }
    return JSONResponse(content=response,  status_code=200)

@app.post("/post_contact_us_data")
def post_contact_us_data(contact_data:schemas.ContactData):
    print(contact_data)
    result = smv_db.post_contact_us_data(contact_data.dict())
    response = {
        "data" : result
    }
    return JSONResponse(content=response, status_code=200)

@app.post("/post_doctor_information_data")
async def post_doctor_information_data(doc_reg_details:schemas.DoctorRegistration):
    print(doc_reg_details)
    result = smv_db.post_doctor_information_data(doc_reg_details.dict())
    print(doc_reg_details.dict())
    response = {
        "data" : result
    }
    return JSONResponse(content=response,  status_code=200)

@app.get("/get_doctor_data")
def get_doctor_data():
    result = smv_db.get_doctor_data()
    response = {
        "data" : result
    }
    return JSONResponse(content=response, status_code=200)

@app.post("/post_appointment_booking_data")
async def post_appointment_booking_data(appointment_data:schemas.AppointmentData): 
    print("Received Data:", appointment_data.dict())
    result = smv_db.post_appointment_booking_data(appointment_data.dict())
    print(appointment_data.dict())
    response = {
        "data" : result
    }
    return JSONResponse(content=response,  status_code=200)

@app.get("/get_doctor_view_data")
def get_doctor_view_data(doctor_id: str = Query(...)):  
    result = smv_db.get_doctor_view_data(doctor_id)
    return JSONResponse(content=result, status_code=200)

@app.get("/get_user_profile")
def get_user_profile(user_id: str = Query(...)):  
    result = smv_db.get_user_profile(user_id)
    if result is None:
        return JSONResponse(content={"error": "User not found"}, status_code=404)    
    return JSONResponse(content=result, status_code=200)

@app.put("/update_user_profile/{user_id}")
async def update_user_profile(user_id: str, user: schemas.UpdateUserProfileSchema):
    try:
        result = smv_db.update_user_profile(user_id, user.dict())  # Ensure user_id is passed correctly
        if result:
            return {"message": "Profile updated successfully"}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_user_history")
def get_user_history(user_id: str = Query(...)):  
    result = smv_db.get_user_history(user_id)
    if result is None:
        return JSONResponse(content={"error": "User not found"}, status_code=404)    
    return JSONResponse(content=result, status_code=200)