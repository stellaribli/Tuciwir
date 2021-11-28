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
import sys
sys.path.insert(0, './src')
from schemas import UserInDB, User, TokenData, Token
from database import db
import os.path

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

cur = db.connect()
 
app = FastAPI(description ="Login Account Tuteers")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashedPassword):
    return pwd_context.verify(plain_password, hashedPassword)

def get_password_hash(password):
    return pwd_context.hash(password)

def makeDateFormat(year: int, month: int, date: int):
    return(str(year)+'-'+str(month)+'-'+str(date))

@app.get('/ambilDataTuteers')
async def ambilSemua(em: str):
    query = "SELECT * FROM tuteers WHERE email = '" + em + "';"
    current_user_query = cur.execute(query)
    return(current_user_query.fetchone())

@app.get('/ambilDataReviewer')
async def ambilSemuaAdmin(em: str):
    query = "SELECT * FROM reviewer WHERE email = '" + em + "';"
    current_user_query = cur.execute(query)
    return(current_user_query.fetchone())

def apakahEmailExistTuteers(email:str):
    query = "SELECT EXISTS(SELECT * from tuteers WHERE email = %s);"
    values = email
    Execute=cur.execute(query,values).fetchone()
    return(Execute[0])

def apakahEmailExistReviewer(email:str):
    query = "SELECT EXISTS(SELECT * from reviewer WHERE email = %s);"
    values = email
    Execute=cur.execute(query,values).fetchone()
    return(Execute[0])

def ambilPassinDB(em:str):
    query = 'SELECT "hashedPassword" FROM tuteers WHERE email = %s;'
    current_user_query = cur.execute(query,em)
    return(current_user_query.fetchone()[0])

def ambilPassinDBRev(em:str):
    query = 'SELECT "hashedPassword" FROM reviewer WHERE email = %s;'
    current_user_query = cur.execute(query,em)
    return(current_user_query.fetchone()[0])

def authenticate_user(email: str, password: str):
    a = False
    if apakahEmailExistTuteers(email):
        passdiDB = ambilPassinDB(email)
        if verify_password(password, passdiDB):
            a = True
    return a

def authenticate_user_reviewer(email: str, password: str):
    a = False
    if apakahEmailExistReviewer(email):
        passdiDB = ambilPassinDBRev(email)
        if verify_password(password, passdiDB):
            a = True
    return a

@app.get('/login', tags = ['User Side'])
async def login (email: str, password: str):
    if authenticate_user(email,password)==True:
        return True
    else:
        return False

@app.get('/loginadmin', tags = ['User Side'])
async def loginadm (email: str, password: str):
    if authenticate_user_reviewer(email,password)==True:
        return True
    else:
        return False

@app.get("/tuteers")
async def gettuteers():
    item = cur.execute('SELECT * FROM tuteers')
    result = item.fetchall()
    return result

@app.get('/resetPasswordSQL/', tags=["Manajemen Akun"])
async def reset_password_sql(passbaru: str, email: str):
    update_formula = 'UPDATE "tuteers" SET "hashedPassword" = %s WHERE "email" = %s'
    values = (get_password_hash(passbaru),email)
    item = cur.execute(update_formula, values)
    return ("Query Update Success")

@app.post('/registerSQL', tags = ['Manajemen Akun'])
async def register_sql(name: str, email: str, password: str, reenterpass: str, noHP: str, year: str, month: str, date: str, gender: str):
    if password == reenterpass:
        tanggal =  makeDateFormat(year,month,date)
        genderStr = gender
        passwordhashed = get_password_hash(password)
        query1 = 'INSERT INTO tuteers ("nama", "email", "noHP", "tanggalLahir", "gender","hashedPassword") VALUES'
        query2 = "(%s,%s,%s,%s,%s,%s);"
        query = query1+query2
        values = (name, email, noHP, tanggal, genderStr, passwordhashed)   
        cur.execute(query, values)
        return('Success')
    else:
        return('Password Tidak Sama!')