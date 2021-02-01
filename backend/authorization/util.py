class ErrorCode:
    AUTHORIZATION_ERROR = 1000


def response(success: bool, message, data, errorCode='', developerMessage=''):
    return {
        "success": success,
        "errorCode": errorCode,
        "message": message,
        "developerMessage": developerMessage,
        "data": data
    }

# {
#     "success": True,
#     "errorCode": 0000,
#     "message": "Retrieved authorization data",
#     "developerMessage": "",
#     "data": {
#           "token": "...",
#           "redirect": "...",
#           "redirectData": { 
#                  ... specific redirect data
#           }  
#     }
# }