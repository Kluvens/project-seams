'''
This file contains all the server functionality for seams.
'''


########################## Import Statements #####################
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.other import clear_v1
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.auth import auth_logout_v1
from src.channels import channels_create_v1, channels_list_v2, channels_listall_v2
from src.channel import channel_details_v1
from src.dms import dm_create_v1
from src.users import user_profile_v1
from src.users import user_setname_v1
from src.users import user_profile_setemail_v1
from src.users import user_profile_sethandle_v1

###################### INITIAL SERVER SETUP ######################

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

###################### Example ###################################
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


################## Authentication and Registration ###############

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
    empty_dict = auth_logout_v1(token)
    return dumps(empty_dict)


########################## Channels ##############################

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



# channels/list/v2
@APP.route('/channels/list/v2', methods=['GET'])
def list():
    paramters_dict = request.get_json()
    return dumps(channels_list_v2(**paramters_dict))

# channels/listall/v2
@APP.route('/channels/listall/v2', methods=['GET'])
def listall():
    paramters_dict = request.get_json()
    return dumps(channels_listall_v2(**paramters_dict))


##################### User routes ############################

# # user/all/v1
# @APP.route('/user/all/v1', methods=['GET'])
# def get_all_users():
#     token = request.get_json()
#     return dumps(user_profile_v1(token))


# user/profile/v1
@APP.route('/user/profile/v1', methods=['GET'])
def profile():
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    u_id = int(u_id)

    return dumps(user_profile_v1(token, int(u_id)))

# user/setname/v1
@APP.route('/user/setname/v1', methods=['PUT'])
def set_name():
    parameters = request.get_json()
    return dumps(user_setname_v1(**parameters))

# user/setname/v1
@APP.route('/user/profile/setemail/v1', methods=['PUT'])
def set_email():
    parameters = request.get_json()
    return dumps(user_profile_setemail_v1(**parameters))

# user/setname/v1
@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def set_handle():
    parameters = request.get_json()
    return dumps(user_profile_sethandle_v1(**parameters))

######################## DMS #####################################

# dm/create/v1 
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    token = request.form.get('token')
    u_ids = request.form.getlist('u_ids')
    u_ids = [int(u_id) for u_id in u_ids]
    return dumps(dm_create_v1(token, u_ids))



####################### CLEARING/RESTTING ########################


# clear/v1
@APP.route("/clear/v1", methods=['DELETE'])
def reset():
    clear_v1()
    return dumps({})



###################### END OF SERVER ROUTES SECTION ################



#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
