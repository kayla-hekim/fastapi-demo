#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os
import mysql.connector
from mysql.connector import Error

DBHOST = 'ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com'
DBUSER = 'ds2022'
DBPASS = os.getenv('DB_PASS')  # Set this in your environment
DB = 'rkf9wd'

api = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get('/genres')
def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        cur.close()
        db.close()
        return(json_data)
    except Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}

@api.get('/songs')
def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = """
    SELECT 
        songs.title AS title,
        songs.album AS album,
        songs.artist AS artist,
        songs.year AS year,
        songs.file AS file,
        songs.image AS image,
        genres.genre AS genre
    FROM 
        songs
    JOIN 
        genres ON songs.genre = genres.genreid
    ORDER BY 
        songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        cur.close()
        db.close()
        return json_data
    except Error as e:
        cur.close()
        db.close()
        return {"Error": "MySQL Error: " + str(e)}



@api.get("/")  # zone apex
def zone_apex():
    return {"Hello": " Kayla Kim"}

@api.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@api.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@api.get("/square/{a}")
def square(a: int):
    return {"square": a * a}

@api.get("/boogieoogie")
def boogieoogie():
    return {"message": "Boogieoogie"}

@api.get("/yesorno/{a}")
def yesorno(a: str):
    if a == "yes":
        return {"message": "yes"}
    else:
        return {"message": "no"}

@api.get("/customer/{idx}")
def customer(idx: int):
    # read the data into a df
    df = pd.read_csv("../customers.csv")
    # filter the data based on the index
    customer = df.iloc[idx] # index locator
    return customer.to_dict()

@api.post("/get_body")
async def get_body(request: Request):
    response =  await request.json()
    first_name = request["fname"]
    last_name = request["lname"]
    favorite_number = request["favnu"]
    return {"first_name": first_name, "last_name": last_name, "favorite_number": favorite_number}

    # return await request.json()
