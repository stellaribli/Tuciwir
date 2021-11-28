from datetime import date, datetime, timedelta
import json
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
# import psycopg2
import sys
sys.path.insert(0, './src')
# import models
from schemas import UserInDB, User, TokenData, Token
from database import db
# import shutil
# import os
import os.path

#     select_formula = 'SELECT "hashed_password" FROM tuteers WHERE "ID_Tuteers" = 1;'
#     item = cur.execute(select_formula)   
#     result = item.fetchone()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

cur = db.connect()
with open("user.json", "r") as read_file:
    fake_users_db = json.load(read_file)
read_file.close()
 
app = FastAPI(description ="Login Account Tuteers")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def makeDateFormat(year: int, month: int, date: int):
    return(str(year)+'-'+str(month)+'-'+str(date))
    
# def ambilAtribut(atribut,em: str):
#     query = "SELECT '" + atribut + "' FROM tuteers WHERE email = '" + em + "';"
#     current_user_query = cur.execute(query)
#     return(current_user_query.fetchone()[0])

def ambilSemua(em: str):
    query = "SELECT * FROM tuteers WHERE email = '" + em + "';"
    current_user_query = cur.execute(query)
    return(current_user_query.fetchone())

@app.get('/ambilpass')
async def ammbilpass(password: str):
    print(verify_password(password, get_password_hash(password)))
    return get_password_hash(password)

def apakahEmailExistTuteers(email:str):
    query = "SELECT EXISTS(SELECT * from tuteers WHERE email = %s);"
    values = email
    Execute=cur.execute(query,values).fetchone()
    return(Execute[0])
print("s")
print (apakahEmailExistTuteers('stella@gmail.com'))
print("ss")
print (apakahEmailExistTuteers('stella@gmaissl.com'))
def ambilPassinDB(em:str):
    query = "SELECT hashed_password FROM tuteers WHERE email = %s;"
    current_user_query = cur.execute(query,em)
    return(current_user_query.fetchone()[0])

# query = "SELECT hashed_password FROM tuteers WHERE email =%s;"
# print (cur.execute(query,'stella@gmail.com').fetchone()[0])

print(ambilPassinDB('stella@gmail.com'))

def authenticate_user(email: str, password: str):
    a = False
    if apakahEmailExistTuteers(email):
        passdiDB = ambilPassinDB(email)
        if verify_password(password, passdiDB):
            a = True
    return a

# print(authenticate_user('stella@gmail.com','asdfe'))
# print (authenticate_user('stella@gmail.com','asdfe'))
# # passdiDB = ambilAtribut('hashed_password','stella@gmail.com')
# print(get_password_hash('a'))
# print(verify_password('asdfe','$2b$12$HN5s5CuFYZX2Ep0qZ9w8jegbTCae6wKIlE7W/UXczHFUrgIkSkdE.'))
# print(verify_password('ab','$2b$12$ren44tB4qrv7S891jgQGZ.dyj0eBYGighoSfdHbRbDLWHSvjBtSWO'))
# print(authenticate_user('stella@gmail.com','asdfe'))

# print(ambilAtribut('hashed_password','stella@gmail.com'))
# print(cur.execute('SELECT * FROM tuteers;').fetchall())

# currentUser = ambilSemua('stella@gmail.com') 

@app.get('/login', tags = ['User Side'])
async def login (email: str, password: str):
    if authenticate_user(email,password)==True:
        return True
    else:
        return False

print("Ssdfsdfa")
print(login("stellaribli@gmail.com","asdf"))
print("Ssdfsdfa")

@app.get("/tuteers")
async def gettuteers():
    item = cur.execute('SELECT * FROM tuteers')
    result = item.fetchall()
    return result

@app.get('/resetPasswordSQL/', tags=["Manajemen Akun"])
async def reset_password_sql(input: str):
    update_formula = 'UPDATE "tuteers" SET "hashed_password" = %s WHERE "ID_Tuteers" = 1'
    values = (get_password_hash(input))
    item = cur.execute(update_formula, values)
    return ("Query Update Success")

@app.post('/registerSQL', tags = ['Manajemen Akun'])
async def register_sql(name: str, email: str, password: str, reenterpass: str, noHP: str, year: str, month: str, date: str, gender: str):
    if password == reenterpass:
        tanggal =  makeDateFormat(year,month,date)
        genderStr = gender
        passwordhashed = get_password_hash(password)
        query1 = 'INSERT INTO tuteers ("nama", "email", "noHP", "tanggalLahir", "gender","hashed_password") VALUES'
        query2 = "(%s,%s,%s,%s,%s,%s);"
        query = query1+query2
        values = (name, email, noHP, tanggal, genderStr, passwordhashed)   
        item = cur.execute(query, values)
        return('Success')
    else:
        return('Password Tidak Sama!')