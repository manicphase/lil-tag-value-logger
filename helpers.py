from datetime import datetime


def dt_to_ts(dt):
    if type(dt) == datetime: return dt
    if not dt: return None
    if type(dt) == datetime:
        return dt
    if type(dt) == float or type(dt) == int:
        print(dt)
        return datetime.fromtimestamp(dt)
    if type(dt) == str:
        try:
            return datetime.fromtimestamp(float(dt))
        except Exception as e:
            print(e)
            pass
    
    try:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    except:
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S").timestamp()