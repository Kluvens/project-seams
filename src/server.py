import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.auth import auth_logout_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.channel import channel_details_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# auth/register/v2 route
@APP.route("/auth/register/v2", methods=['POST'])
def register():
    paramters_dict = request.get_json()
    return dumps(auth_register_v1(**paramters_dict))


# auth/login/v2 route
@APP.route("/auth/login/v2", methods=['POST'])
def login():
    paramters_dict = request.get_json()
    return dumps(auth_login_v1(**paramters_dict))


# auth/logout/v1 route
@APP.route("/auth/logout/v1", methods=['POST'])
def logout():
    token = request.get_json()
    empty_dict = auth_logout_v1(str(token))
    return dumps(empty_dict)

# channel/create/v2 route
@APP.route("/channels/create/v2", methods=['POST'])
def create():
    parameters = request.get_json()
    return dumps(channels_create_v1(**parameters))

# channel/details/v2
@APP.route("/channel/details/v2", methods = ['GET'])
def channel_details_http():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel_details_v1(token, channel_id))

# clear/v1
@APP.route("/clear/v1", methods=['DELETE'])
def reset():
    clear_v1()
    return dumps({})


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
