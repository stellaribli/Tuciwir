from re import search
from typing import List
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import psycopg2
import sys

from starlette.responses import Response
sys.path.insert(0, './src')
import models
import schemas
from database import db
from fastapi.responses import FileResponse
import shutil
import json
import os
import os.path

models.Base.metadata.create_all(bind=db)

app = FastAPI()


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

cur = db.connect()

cur_booking_id = 0
# API Endpoints

# Upload, Download Module
@app.patch('/upload-cv/', tags=['Uploader'])
async def upload_cv(booking_id: int, uploaded_file: UploadFile = File(...)):
    file_path = f"./cv_tuteers/{uploaded_file.filename}"
    file_location = uniquify(file_path)
    item_found = False

    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    if result != None:
        if result[0] == booking_id:
            if result[3] == None:
                # cv blm ada
                item_found = True
                alter_formula = 'UPDATE booking SET cv = %s WHERE "ID_Booking" = %s'
                values = (file_location, booking_id)
                try:
                    with open(file_location, "wb+") as file_object:
                        shutil.copyfileobj(uploaded_file.file, file_object)
                    cur.execute(alter_formula, values)
                except:
                     raise HTTPException(
                         status_code=404, detail=f'There was an error!')
            else:
                return {"message": "CV exists!"}
    if item_found:
        return {"message": f"file '{uploaded_file.filename}' uploaded for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Booking not found!')
    
   
@app.patch("/upload-review/", tags=['Uploader'])
async def upload_review(booking_id: int, reviewer_id: int, uploaded_file: UploadFile = File(...)):
    file_path = f"./hasil_review/{uploaded_file.filename}"
    file_location = uniquify(file_path)
    item_found = False

    search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
    search_value = (booking_id, reviewer_id)
    item = cur.execute(search_formula, search_value)
    result = item.fetchone()
    print(result)
    if result != None:
        if result[0] == reviewer_id and result[1] == booking_id:
            if result[2] == None:
                # cv blm ada
                item_found = True
                alter_formula = 'UPDATE review SET "Hasil_Review" = %s, "isDone" = true WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
                values = (file_location, booking_id, reviewer_id)
                try:
                    with open(file_location, "wb+") as file_object:
                        shutil.copyfileobj(uploaded_file.file, file_object)
                    cur.execute(alter_formula, values)
                except:
                     raise HTTPException(
                         status_code=404, detail=f'There was an error!')
            else:
                return {"message": "Review exists!"}
    if item_found:
        return {"message": f"Review file '{uploaded_file.filename}' uploaded for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Review not found!')

@app.get("/download-cv/", tags=['Downloader'])
async def download_tuteers_cv(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    if result != None:
        if result[0] == booking_id:
            item_found = True
            if result[3] == None:
                #cv belum ada
                return {"message": "CV doesn't exist!"}
            else:
                path = result[3]
                filename = "CV_IDBooking_" + str(result[0]) + ".pdf"
    if item_found:
        return FileResponse(path=path, filename=filename, media_type='application/pdf')
    raise HTTPException(
        status_code=404, detail=f'Booking did not exist!')


@app.get("/download-cv-review/", tags=['Downloader'])
async def download_review_cv(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    print(result)
    if result != None:
         if result[0] == booking_id:
            item_found = True
            if result[2] == None:
                #review belum ada
                return {"message": "Review isn't available yet!"}
            else:
                path = result[2]
                filename = "ReviewCV_IDBooking_" + str(result[1]) + ".pdf"
    if item_found:
        return FileResponse(path=path, filename=filename, media_type='application/pdf')
    raise HTTPException(
        status_code=404, detail=f'CV Review doesnt exists!')


@app.patch('/remove-cv-from-booking/', tags=['Delete'])
async def remove_cv_from_booking(booking_id: int):
    item_found = False
    search_formula = 'SELECT * FROM booking WHERE "ID_Booking" = %s'
    item = cur.execute(search_formula, booking_id)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[3] == None:
            return {"message" : "There is no CV yet!"}
        else:
            file_location = result[3]
            try:
                nullify = 'UPDATE booking SET "cv" = NULL WHERE "ID_Booking" = %s'
                value = (booking_id)
                cur.execute(nullify, value)
                os.remove(file_location)
            except:
                return {"message": "There is an error!"}

    if item_found:
        return {"message": f"CV file has been deleted for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Booking not found!')

@app.patch('/delete-review/', tags=['Delete'])
async def remove_cv_from_review(booking_id: int, reviewer_id: int):
    item_found = False
    search_formula = 'SELECT * FROM review WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
    values = (booking_id, reviewer_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[2] == None:
            return {"message" : "There is no Review yet!"}
        else:
            file_location = result[2]
            try:
                nullify = 'UPDATE review SET "Hasil_Review" = NULL, "isDone" = False WHERE "ID_Booking" = %s and "ID_Reviewer" = %s'
                value = (booking_id, reviewer_id)
                cur.execute(nullify, value)
                os.remove(file_location)
            except:
                return {"message": "There is an error!"}
    if item_found:
        return {"message": f"CV review file has been deleted for booking number: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Review not found!')

@app.get("/booking", tags=["Get"])
async def get_all_booking():
    item = cur.execute('SELECT * FROM booking')
    result = item.fetchall()
    return result


@app.get("/review", tags=["Get"])
async def get_all_review():
    item = cur.execute('SELECT * FROM review')
    result = item.fetchall()
    return result

@app.get("/paket", tags=["Get"])
async def get_all_paket():
    item = cur.execute('SELECT * FROM paket')
    result = item.fetchall()
    return result

@app.get("/paket/{paket_id}", tags=["Get"])
async def get_paket(paket_id: int):
    item_found = False
    search_formula = 'SELECT * FROM paket WHERE "ID_Paket" = %s'
    values = (paket_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[0] == paket_id:
            return result
            
    if item_found:
        return {"message": f"Paket: {paket_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Paket not found!')

# @app.get("/paket/{paket_id}", tags=["Get"])
# async def get_paket(paket_id: int):
#     search_formula = 'SELECT * FROM paket WHERE "ID_Paket" = %s'
#     values = (paket_id)
#     item = cur.execute(search_formula, values)
#     result = item.fetchone()
#     if result[0] != paket_id:
#         return{"message" : "Package not available"}
#     else:
#         return result
            
@app.get("/Booking/{tuteers_id}", tags=["Get"])
async def get_booking_by_tuteers_id(tuteers_id: int):
    item_found = False
    booking_id = cur_booking_id
    search_formula = 'SELECT * FROM booking WHERE "ID_Tuteers" = %s'
    values = (tuteers_id)
    item = cur.execute(search_formula, values)
    result = item.fetchone()
    if result != None:
        item_found = True
        if result[2] == tuteers_id:
            booking_id = result[0]
            return result

    if item_found:
        return {"message": f"Booking_id: {booking_id}'"}
    raise HTTPException(
		status_code=404, detail=f'Tuteers Booking not found!')
    
@app.post("/create-booking", tags=["Add"])
#async def add_booking(paket_id: int, current_user: User = Depends(get_current_active_user)):
async def add_booking(paket_id: int, tuteers_id: int):
    try:
        item = cur.execute('select "ID_Booking" from booking order by "ID_Booking" DESC LIMIT 1')
        current_booking_id = item.fetchone()[0]
    except:
        raise HTTPException(
		    status_code=404, detail=f'wuery satu gajalan')
    booking_id = int(current_booking_id)+1
    add_formula = 'INSERT INTO booking ("ID_Booking", "ID_Paket", "ID_Tuteers", "tgl_pesan") values (%s, %s, %s, current_timestamp)'
    values = (booking_id, paket_id, tuteers_id)
    try:
        item2 = cur.execute(add_formula, values)
    except Exception as E:
        print(E)
        # raise HTTPException(
		#     status_code=404, detail=f'query 2 gajalan')
    return {"message" : "Berhasil menambahkan booking dengan id booking" +str(booking_id)}