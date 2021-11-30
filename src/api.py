from datetime import date, datetime, timedelta
import json

from sqlalchemy.sql.expression import false
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.sql.sqltypes import BLOB, Date
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

@app.get("/users/me/", response_model=User, tags=["Initiate"])
# async def Data_User(current_user: User = Depends(get_current_active_user)):
async def Data_User():
    return current_user

#DIPAKE
#booking yg direview current user HARUSNYA YG INI TP BLM ADA CURR USER
# @app.get("/booking", tags=["Booking"])
# async def get_booking_by_reviewer(reviewer_id: int):
#     values = (reviewer_id)
#     item = cur.execute('SELECT b."ID_Booking", DATE(b."tgl_pesan") as tgl, r."isDone" FROM review r, booking b WHERE r."ID_Reviewer" = %s and r."ID_Booking" = b."ID_Booking"', values)
#     result = item.fetchall()
#     return result

@app.get('/booking/', tags=["All"])
async def booking():
    item = cur.execute('SELECT * FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking"')
    result = item.fetchall()
    return result

@app.get('/review/', tags=["All"])
async def review():
    item = cur.execute('SELECT b."ID_Booking", DATE(b."tgl_pesan") as tgl, r."isDone" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking" AND r."ID_Reviewer"=%s', values)
    result = item.fetchall()
    return result

@app.get('/reviewerbookingdia', tags=["ReviewCV"])
# async def read_all_booking(current_user: User = Depends(get_current_active_user)):
async def review_booking(id_reviewer:int):
    values = (id_reviewer)
    item = cur.execute('SELECT b."ID_Booking", DATE(b."tgl_pesan") as tgl, r."isDone" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking" AND r."ID_Reviewer"=%s', values)
    result = item.fetchall()
    return result

#halaman awal booking yg blm direview siapapun
@app.get('/reviewerbooking', tags=["ReviewCV"])
# async def read_all_booking(current_user: User = Depends(get_current_active_user)):
async def read_all_booking():
    item = cur.execute('SELECT "ID_Booking", DATE("tgl_pesan") as tgl FROM booking WHERE "ID_Booking" NOT IN (SELECT b."ID_Booking" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking")')
    result = item.fetchall()
    return result

#pilih booking
@app.post('/reviewerpilihbooking', tags=["ReviewCV"])
async def choose_booking(id_booking:int, id_reviewer:int):
    values = (id_reviewer,id_booking)
    query = 'INSERT INTO review ("ID_Reviewer", "ID_Booking", "isDone") VALUES (%s,%s,false)'
    item = cur.execute(query, values)
    return item

# reviewer download cv
@app.get('/reviewerdownloadcv/id_reviewer={id_reviewer}&id_booking={id_booking}', tags=["ReviewCV"])
async def download_booking(id_booking:int, id_reviewer:int):
    values = (id_reviewer,id_booking)
    query = 'SELECT b."cv" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking" AND r."ID_Reviewer"=%s AND r."ID_Booking"=%s'
    item = cur.execute(query, values)
    result = item.fetchall()
    return result

#-----------------------------------------------------------------------

# @app.get('/review', tags=["Booking"])
# async def read_all_review():
#     item = cur.execute('SELECT * FROM review')
#     result = item.fetchall()
#     return result
