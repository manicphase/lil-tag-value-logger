from datetime import datetime
import time
import models


def get(session_id, recording_id,  tags, db):
    negative_tags = []
    positive_tags = []
    if tags:
        negative_tags = [t[1:] for t in tags if t.startswith("-")]
        positive_tags = [t for t in tags if not t.startswith("-")]
    query = db.query(models.Entry)
    if session_id:
        query = query.filter(models.Entry.session_id == session_id)
    if recording_id:
        query = query.filter(models.Entry.recording_id == recording_id)
    result = query.all()
    if not positive_tags:
        positive_tags = set([r.tag for r in result])
    for t in negative_tags:
        if t in positive_tags:
            positive_tags.remove(t)
    tags = positive_tags
    tagged_dict = { tag: [r for r in result if r.tag == tag] for tag in tags}
    results = [{"tag": tag, "results": tagged_dict[tag]} for tag in tagged_dict.keys()]
    #import ipdb; ipdb.set_trace()
    return results

def add(tag, value, session_id, recording_id, db):
    entry_dict = {
        "tag": tag,
        "value": value,
        "session_id": session_id,
        "recording_id": recording_id,
        "timestamp": datetime.now()
    }

    db_item = models.Entry(**entry_dict)
    db.add(db_item)
    db.commit()
    return #get(db)

def save_session_data(name, data, db):
    db_item = models.GraphingSession(name=name, data=data)
    db.add(db_item)
    db.commit()
    return

def get_sessions(db):
    return db.query(models.GraphingSession).all()

def delete_session(session_id, db):
    db.query(models.GraphingSession).filter(models.GraphingSession.id==session_id).delete()
    db.commit()