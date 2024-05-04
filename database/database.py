import json
from redis import Redis

r = Redis(host='localhost', 
                port=6379, 
                charset="utf-8",
                decode_responses=True)

def load(name):
    type_data = r.type(name)
    if type_data =='list':
        result = r.lrange(name, 0, -1)
    
    elif type_data == 'hash':
        all_fields = r.hgetall(name)
        
        result = dict()
        for id, fields in all_fields.items():
            result[id] = json.loads(fields)
    
    r.close()   
    return result

def save(name, data):
    type_data = r.type(name)
    if type_data == 'list' or isinstance(data, list):
        r.delete(name)
        r.rpush(name, *data)

    elif type_data == 'hash' or isinstance(data, dict):
        for item, value in data.items():
            r.hset(name, item, json.dumps(value))
    
    r.close()