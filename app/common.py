import time,datetime,calendar
import os
import base64


class STATUS:
    
    OK            = 0 # all ok
    ERR           = 1 # generic err 
    ERR_AUTH      = 2 # auth err
    ERR_INPUT     = 3 # wrong input 

# Class for constants & data types ..
class COMMON:

    NOT_SET    = -1

class DATATYPE:
    NOT_SET    = -1
    TEXT       =  0
    HTML       =  1
    JSON       =  2
    COUNT      =  3
    OBJ_TYPE   =  4
    CRYPTED    =  5
    

