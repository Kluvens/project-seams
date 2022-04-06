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
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.channel import channel_invite_v2, channel_join_v2
from src.channel import channel_details_v2, channel_messages_v2
from src.channel import channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.other import clear_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.dm import dm_messages_v1
from src.dms import dm_create_v1, dm_list_v1, dm_details_v1, dm_leave_v1, dm_remove_v1
from src.message import message_senddm_v1
from src.users import users_all_v1
from src.users import user_profile_v1
from src.users import user_setname_v1
from src.users import user_profile_setemail_v1
from src.users import user_profile_sethandle_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1, message_senddm_v1

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
# @APP.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })

############################## AUTH ##############################
@APP.route("/auth/register/v2", methods = ['POST'])
def auth_register_http():
    register_dict = request.get_json()

    return dumps(auth_register_v2(**register_dict))

@APP.route("/auth/login/v2", methods = ['POST'])
def auth_login_http():
    login_dict = request.get_json()

    token = auth_login_v2(**login_dict)
    return dumps(token)

@APP.route("/auth/logout/v1", methods = ['POST'])
def auth_logout_http():
    token = request.get_json()['token']
    auth_logout_v1(token)

    return dumps({})

############################ Channel ############################
@APP.route("/channel/invite/v2", methods = ['POST'])
def channel_invite_http():
    invite_dict = request.get_json()
    channel_invite_v2(**invite_dict)
    
    return dumps({})

@APP.route("/channel/details/v2", methods = ['GET'])
def channel_details_http():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    return dumps(channel_details_v2(token, channel_id))

@APP.route("/channel/join/v2", methods = ['POST'])
def channel_join_http():
    return_list = request.get_json()
    
    return dumps(channel_join_v2(**return_list))

@APP.route("/channel/leave/v1", methods = ['POST'])
def channel_leave_https():
    return_list = request.get_json()

    return dumps(channel_leave_v1(**return_list))

@APP.route("/channel/addowner/v1", methods = ['POST'])
def channel_addowner_http():
    return_list = request.get_json()
    channel_addowner_v1(**return_list)

    return dumps({})

@APP.route("/channel/removeowner/v1", methods = ['POST'])
def channel_removeowner_http():
    return_list = request.get_json()
    channel_removeowner_v1(**return_list)

    return dumps({})

@APP.route("/channels/list/v2", methods = ['GET'])
def channels_list_http():
    token = request.args.get('token')
    return dumps(channels_list_v2(token))

@APP.route("/channels/listall/v2", methods = ['GET'])
def channels_listall_http():
    token = request.args.get('token')
    return dumps(channels_listall_v2(token))

@APP.route("/channels/create/v2", methods = ['POST'])
def channels_create_http():
    create_dict = request.get_json()

    return dumps(channels_create_v2(**create_dict))

############################## DMS ##############################
# dm/list/v1
@APP.route('/dm/list/v1', methods=['GET'])
def dm_list_http():
    token = request.args.get('token')
    return dumps(dm_list_v1(token))

# dm/create/v1 route
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_http():
    data = request.get_json()
    u_ids = data['u_ids']
    token = data['token']
    return dumps(dm_create_v1(token, u_ids))

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove_http():
    return_list = request.get_json()
    return dumps(dm_remove_v1(**return_list))

# dm/details/v1
@APP.route("/dm/details/v1", methods = ['GET'])
def dm_details_http():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    return dumps(dm_details_v1(token, dm_id))


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_http():
    return_list = request.get_json()
    return dumps(dm_leave_v1(**return_list))

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm_http():
    message_info = request.get_json()
    token = message_info['token']
    dm_id = message_info['dm_id']
    message = message_info['message']
    return dumps(message_senddm_v1(token, dm_id, message))

############################# Admin #############################
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_http():
    return_dict = request.get_json()
    return dumps(admin_user_remove_v1(**return_dict))

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_http():
    return_dict = request.get_json()
    return dumps(admin_userpermission_change_v1(**return_dict))

############################# Users #############################
# user/all/v1
@APP.route('/users/all/v1', methods=['GET'])
def get_all_users():
    token = request.args.get("token")
    return dumps(users_all_v1(token))

# user/profile/v1
@APP.route('/user/profile/v1', methods=['GET'])
def profile():
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    u_id = int(u_id)

    return dumps(user_profile_v1(token, int(u_id)))

# user/profile/setname/v1
@APP.route('/user/profile/setname/v1', methods=['PUT'])
def set_name():
    parameters = request.get_json()
    return dumps(user_setname_v1(**parameters))

# user/profile/setemail/v1
@APP.route('/user/profile/setemail/v1', methods=['PUT'])
def set_email():
    parameters = request.get_json()
    return dumps(user_profile_setemail_v1(**parameters))

# user/profile/sethandle/v1
@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def set_handle():
    parameters = request.get_json()
    return dumps(user_profile_sethandle_v1(**parameters))

########################## Messages ##########################

# channel/messages/v2
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    # write_savefile()
    return dumps(channel_messages_v2(token, channel_id, start))

# message/send/v1
@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    data = request.get_json()
    # FRONT-END PROBLEM - supplying an extra parameter
    token = data["token"]
    channel_id = data["channel_id"]
    message = data["message"]
    return dumps(message_send_v1(token, channel_id, message))

# message/remove/v1
@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    message_remove_v1(**data)
    # write_savefile()
    return dumps({})

# dm/messages/v1
@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')
    # write_savefile()
    return dumps(dm_messages_v1(token, dm_id, start))

# message/edit/v1
@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    data = request.get_json()
    message_edit_v1(**data)
    # write_savefile()
    return dumps({})

# load_savefile()

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

