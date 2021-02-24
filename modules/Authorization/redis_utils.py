#!/usr/bin/env python
"""
This script contains various tools for the usage of the Redis cloud
"""

import redis
import json


redis_instance = None
redis_host = 'redis-18794.c93.us-east-1-3.ec2.cloud.redislabs.com'
redis_port = 18794
redis_password = 'BnxpmnasfwiT5JsJmVTqENI6An7EH6ew'

def get_connexion():
    """Gets connexion to redis cloud

    Returns:
        redis.Redis: redis instance
    """    
    global redis_instance
    if redis_instance == None:
        redis_instance = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
    return redis_instance
def put(key, value):
    """Puts a key value pair into redis

    Args:
        key (string): Redis document name
        value (string): string object
    """    

    response = get_connexion().execute_command('SET', key, value)
def get(key):
    """Retrieves a value from redis using a key

    Args:
        key (string): Redis document name

    Returns:
        string: Stringified json value
    """    
    redis_value_type = get_connexion().type(key).decode("utf-8")
    value = None
    if redis_value_type == 'string':
        value = get_connexion().execute_command('GET', key).decode("utf-8")
    elif redis_value_type == 'hash':
        value = get_connexion().execute_command('HGETALL', key)
    else:
        print("No retrieve function for this type: ", redis_value_type) 
    return value
def expire(key, timeout):
    """Sets an expiration to a redis document

    Args:
        key (string): Redis document name
        timeout (integer): Timeout value in seconds
    """    
    get_connexion().expire(key, timeout)
def remove(key):
    """Removes a redis document

    Args:
        key (string): Redis document name
    """    
    get_connexion().delete(key)
def test_connexion(verbose=False):
    """Tests the connexion to the Redis cloud

    Args:
        verbose (bool, optional): If true additional logs will be activated for debug purposes. Defaults to False.

    Returns:
        [type]: [description]
    """    
    try:
        get_connexion().ping()
    except Exception as e:
        print(e)
        return False
    if verbose:
        print("Sucessfully connected to Redis")
    return True
def dumpAll(verbose=True):
    return [(x.decode("utf-8"), get(x.decode("utf-8")))  for x in get_connexion().keys()]

def example():
    """Example method for testing purposes
    """    
    value = {
        'foo': 'bar'
    }

    key = 'example'

    if not test_connexion():
        exit(-1)
    print('Put value in ' + key)
    put(value, key)
    reply = get(key)
    print('value: ' + str(reply))

    print('Remove value from ' + key)
    remove(key)
    reply = get(key)
    print('value: ' + str(reply))


if __name__ == '__main__':
    example()