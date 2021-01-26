# Responsible for the authorization / gateway

# Features
# Fetch the request and extract the opaque token from it
# Retrieve user session data from Redis

# https://hackernoon.com/doing-microservices-user-sessions-right-the-fundamentals-hj3z34nu

from generate_unique_id import generate_session_id
import redis_utils as r

class SessionManager:
    SESSION_TIMEOUT_KEY = 'session.timeout'
    SESSION_TIMEOUT_DEFAULT = 1800 # 30 minutes
    
    @staticmethod
    def create(String sessionData):
        sessionId = generate_session_id()
        SessionManager.update(sessionId, sessionData)
        return sessionId

    @staticmethod
    def update(sessionId, sessionData):
        r.put(sessionId, sessionData)
        r.expire(sessionId, getSessionTimeout())

    @staticmethod
    def get(sessionId):
        sessionData = r.get(sessionId)
        if sessionData is not None:
            r.expire(sessionId, getSessionTimeout())
        return sessionData
    
    @staticmethod
    def refresh(sessionId):
        r.expire(sessionId, getSessionTimeout())

    @staticmethod
    def remove(sessionId):
        r.remove(sessionId)

    @staticmethod
    def setSessionTimeout(timeout=SESSION_TIMEOUT_DEFAULT):
        r.set(SessionManager.SESSION_TIMEOUT_KEY, timeout)

    @staticmethod
    def getSessionTimeout():
        timeout = r.get(SessionManager.SESSION_TIMEOUT_KEY)
        if timeout is None:
            timeout = SESSION_TIMEOUT_DEFAULT
            setSessionTimeout(timeout)
        return int(timeout)
