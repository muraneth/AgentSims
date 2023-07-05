from datetime import datetime
import time
import json


# Load a json file and return the json object.
def load_json_file(path):
    # Open json file.
    f = open(path)
    # Read json object from file.
    obj = json.load(f)
    # Close file.
    f.close()
    # Return json object.
    return obj


def get_json_value(obj, key, default):
    if key in obj:
        return obj[key]
    return default

def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)

def format_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

def datetime_to_timestamp(dt: datetime) -> int:
    return int(time.mktime(dt.timetuple()))

def get_idle_id(array, min=1, max=10000):
    i = min
    for i in range(min, max+1):
        found = False
        for item in array:
            if item.id == i:
                found = True
                break
        if not found:
            break
    return i

if __name__ == "__main__":
    print(time.time())
    print(datetime_to_timestamp(timestamp_to_datetime(time.time())))
