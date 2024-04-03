import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

import time
import crud
import models

router = APIRouter()

from db.database import get_db
from helpers import dt_to_ts

global last_update
global session_id
last_update = 0
session_id = 0

def get_session_id(db):
    global last_update
    global session_id

    if last_update < time.time() - 10:
        last = db.query(models.Entry).order_by(models.Entry.id.desc()).first()
        if last:
            session_id = last.session_id
            print("got session id from db")
        session_id += 1
    last_update = time.time()

@router.get("/add")
def add_entry(tag=None, value=None, recording_id=None, db: Session=Depends(get_db)):
    global last_update
    global session_id
    get_session_id(db)
    crud.add(tag, value, session_id, recording_id, db)
    print(f"tag: {tag} | value: {value}")
    return session_id

@router.get("/get")
def get_entries(session_id=None, recording_id=None, tags=None, db: Session=Depends(get_db)):
    if tags: tags = tags.split(",")
    results = crud.get(session_id, recording_id, tags, db)
    return results

@router.get("/get_result_count")
def get_result_count(session_id=None, recording_id=None, tags=None, db: Session=Depends(get_db)):
    entries = get_entries(session_id, recording_id, tags, db)
    count = len(entries[0]["results"])
    print(f"COUNT={count}")
    return count

@router.get("/single_result")
def get_single_result(session_id=None, recording_id=None, tags=None, index=0, db: Session=Depends(get_db)):
    entries = get_entries(session_id, recording_id, tags, db)
    value = entries[0]["results"][int(float(index))].value
    print(f"VALUE={value}")
    return value


@router.post("/graphing_session")
async def save_graphing_session(session_data: Request, db: Session=Depends(get_db)):
    result = await session_data.json()
    name = result["name"]
    data = result["data"]
    crud.save_session_data(name, data, db)

@router.get("/graphing_session")
def get_graphing_sessions(db: Session=Depends(get_db)):
    result = crud.get_sessions(db)
    for r in result:
        r.data = json.loads(r.data)
    return result

@router.delete("/graphing_session")
async def delete_graphing_sessions(session_data: Request, db: Session=Depends(get_db)):
    to_delete = await session_data.json()
    crud.delete_session(to_delete["graph_id"], db)
    result = crud.get_sessions(db)
    for r in result:
        r.data = json.loads(r.data)
    return result