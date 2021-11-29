from datetime import date, datetime, timedelta
import json

from sqlalchemy.sql.expression import false
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.sql.sqltypes import Date
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from re import search
from fastapi import Depends, FastAPI, HTTPException
import psycopg2
import sys
sys.path.insert(0, './src')
import models
from schemas import UserInDB, User, TokenData, Token
from database import db
import shutil
import os
import os.path

cur = db.connect()

SECRET_KEY = "95be5a51fa29a6cf400f4e60684b0594bb77260916151c09a7fd39613316cc4b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(description ="Login Account Tuteers")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# dummy_user = {
#     "asdf": {
#         "username": "asdf",
#         "hashed_password": "$2b$12$ozaFLkFGK59YlwU/wOQU..0dpBQGCb5tceg1PJEEXMnQxnOCmZz6q",
#         "disabled": False,
#     }
# }

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class User(BaseModel):
#     username: str
#     disabled: Optional[bool] = None

# class UserInDB(User):
#     hashed_password: str

# with open("booking.json","r") as read_file:
# 	data=json.load(read_file)
# app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(dummy_user, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# @app.get("/", tags=["Initiate"])
# async def Nama_NIM():
#     return("Nama: Zarfa Naida P, NIM: 18219014, Silahkan buka: http://zarfanpr-tst2.herokuapp.com/docs")

# @app.post("/token", response_model=Token, tags=["Initiate"])
# async def login_untuk_akes_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(dummy_user, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User, tags=["Initiate"])
# async def Data_User(current_user: User = Depends(get_current_active_user)):
async def Data_User():
    return current_user

@app.get('/booking', tags=["Booking"])
# async def read_all_booking(current_user: User = Depends(get_current_active_user)):
async def review_booking():
    item = cur.execute('SELECT b."ID_Booking", b."tgl_pesan", r."isDone" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking"')
    result = item.fetchall()
    return result

@app.get('/bookingall', tags=["Booking"])
# async def read_all_booking(current_user: User = Depends(get_current_active_user)):
async def read_all_booking():
    item = cur.execute('SELECT "ID_Booking", "tgl_pesan" FROM booking')
    result = item.fetchall()
    return result

@app.get('/review', tags=["Booking"])
async def read_all_review():
    item = cur.execute('SELECT * FROM review')
    result = item.fetchall()
    return result

@app.get("/review/", tags=["Booking"])
async def get_booking_by_reviewer(reviewer_id: int):
    values = (reviewer_id)
    item = cur.execute('SELECT * FROM review r, booking b WHERE r."ID_Reviewer" = %s and r."ID_Booking" = b."ID_Booking"', values)
    result = item.fetchall()
    return result

@app.post('/booking/{id_booking}', tags=["Booking"])
async def choose_booking(id_booking:int, id_reviewer:int):
    values = (id_reviewer,id_booking)
    query = 'INSERT INTO review ("ID_Reviewer", "ID_Booking", "isDone") VALUES (%s,%s,false)'
    item = cur.execute(query, values)
    return('Success')

# from re import search
# from typing import List
# from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
# from sqlalchemy.orm import Session
# import psycopg2
# import sys
# sys.path.insert(0, './src')
# import models
# import schemas
# from database import db
# from fastapi.responses import FileResponse
# import shutil
# import json
# import os
# import os.path

# models.Base.metadata.create_all(bind=db)

# app = FastAPI()


# def uniquify(path):
#     filename, extension = os.path.splitext(path)
#     counter = 1

#     while os.path.exists(path):
#         path = filename + " (" + str(counter) + ")" + extension
#         counter += 1

#     return path

# cur = db.connect()

# # API Endpoints

# # Upload, Download Module
# @app.patch('/upload-cv/', tags=['Uploader'])
# async def upload_cv(booking_id: int, uploaded_file: UploadFile = File(...)):
#     file_path = f"./cv_tuteers/{uploaded_file.filename}"
#     file_location = uniquify(file_path)
#     item_found = False

#     search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
#     item = cur.execute(search_formula, booking_id)
#     result = item.fetchone()
#     if result != None:
#         if result[0] == booking_id:
#             if result[3] == None:
#                 # cv blm ada
#                 item_found = True
#                 alter_formula = 'UPDATE booking SET cv = %s WHERE "ID_Booking" = %s'
#                 values = (file_location, booking_id)
#                 try:
#                     with open(file_location, "wb+") as file_object:
#                         shutil.copyfileobj(uploaded_file.file, file_object)
#                     cur.execute(alter_formula, values)
#                 except:
#                      raise HTTPException(
#                          status_code=404, detail=f'There was an error!')
#             else:
#                 return {"message": "CV exists!"}
#     if item_found:
#         return {"message": f"file '{uploaded_file.filename}' uploaded for booking number: {booking_id}'"}
#     raise HTTPException(
# 		status_code=404, detail=f'Booking not found!')
    
   
# @app.patch("/upload-review/", tags=['Uploader'])
# async def upload_review(booking_id: int, reviewer_id: int, uploaded_file: UploadFile = File(...)):
#     file_path = f"./hasil_review/{uploaded_file.filename}"
#     file_location = uniquify(file_path)
#     item_found = False

#     search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
#     search_value = (booking_id, reviewer_id)
#     item = cur.execute(search_formula, search_value)
#     result = item.fetchone()
#     print(result)
#     if result != None:
#         if result[0] == reviewer_id and result[1] == booking_id:
#             if result[2] == None:
#                 # cv blm ada
#                 item_found = True
#                 alter_formula = 'UPDATE review SET "Hasil_Review" = %s, "isDone" = true WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
#                 values = (file_location, booking_id, reviewer_id)
#                 try:
#                     with open(file_location, "wb+") as file_object:
#                         shutil.copyfileobj(uploaded_file.file, file_object)
#                     cur.execute(alter_formula, values)
#                 except:
#                      raise HTTPException(
#                          status_code=404, detail=f'There was an error!')
#             else:
#                 return {"message": "Review exists!"}
#     if item_found:
#         return {"message": f"Review file '{uploaded_file.filename}' uploaded for booking number: {booking_id}'"}
#     raise HTTPException(
# 		status_code=404, detail=f'Review not found!')

# @app.get("/download-cv/", tags=['Downloader'])
# async def download_tuteers_cv(booking_id: int):
#     item_found = False
#     search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
#     item = cur.execute(search_formula, booking_id)
#     result = item.fetchone()
#     if result != None:
#         if result[0] == booking_id:
#             item_found = True
#             if result[3] == None:
#                 #cv belum ada
#                 return {"message": "CV doesn't exist!"}
#             else:
#                 path = result[3]
#                 filename = "CV_IDBooking_" + str(result[0]) + ".pdf"
#     if item_found:
#         return FileResponse(path=path, filename=filename, media_type='application/pdf')
#     raise HTTPException(
#         status_code=404, detail=f'Booking did not exist!')


# @app.get("/download-cv-review/", tags=['Downloader'])
# async def download_review_cv(booking_id: int):
#     item_found = False
#     search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s'
#     item = cur.execute(search_formula, booking_id)
#     result = item.fetchone()
#     print(result)
#     if result != None:
#          if result[0] == booking_id:
#             item_found = True
#             if result[2] == None:
#                 #review belum ada
#                 return {"message": "Review isn't available yet!"}
#             else:
#                 path = result[2]
#                 filename = "ReviewCV_IDBooking_" + str(result[1]) + ".pdf"
#     if item_found:
#         return FileResponse(path=path, filename=filename, media_type='application/pdf')
#     raise HTTPException(
#         status_code=404, detail=f'CV Review doesnt exists!')


# @app.patch('/remove-cv-from-booking/', tags=['Delete'])
# async def remove_cv_from_booking(booking_id: int):
#     item_found = False
#     search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
#     item = cur.execute(search_formula, booking_id)
#     result = item.fetchone()
#     if result != None:
#         item_found = True
#         if result[3] == None:
#             return {"message" : "There is no CV yet!"}
#         else:
#             file_location = result[3]
#             try:
#                 nullify = 'UPDATE booking SET "cv" = NULL WHERE "ID_Booking" = %s'
#                 value = (booking_id)
#                 cur.execute(nullify, value)
#                 os.remove(file_location)
#             except:
#                 return {"message": "There is an error!"}

#     if item_found:
#         return {"message": f"CV file has been deleted for booking number: {booking_id}'"}
#     raise HTTPException(
# 		status_code=404, detail=f'Booking not found!')


# @app.patch('/delete-review/', tags=['Delete'])
# async def remove_cv_from_review(booking_id: int, reviewer_id: int):
#     item_found = False
#     search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
#     values = (booking_id, reviewer_id)
#     item = cur.execute(search_formula, values)
#     result = item.fetchone()
#     if result != None:
#         item_found = True
#         if result[2] == None:
#             return {"message" : "There is no Review yet!"}
#         else:
#             file_location = result[2]
#             try:
#                 nullify = 'UPDATE review SET "Hasil_Review" = NULL, "isDone" = False WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
#                 value = (booking_id, reviewer_id)
#                 cur.execute(nullify, value)
#                 os.remove(file_location)
#             except:
#                 return {"message": "There is an error!"}
#     if item_found:
#         return {"message": f"CV review file has been deleted for booking number: {booking_id}'"}
#     raise HTTPException(
# 		status_code=404, detail=f'Review not found!')

# @app.get("/booking", tags=["Get"])
# async def get_all_booking():
#     item = cur.execute('SELECT * FROM booking')
#     result = item.fetchall()
#     return result


# @app.get("/review", tags=["Get"])
# async def get_all_review():
#     item = cur.execute('SELECT * FROM review')
#     result = item.fetchall()
#     return result


