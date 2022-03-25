import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v2, auth_register_v2
from src.channel import channel_invite_v1, channel_join_v1, channel_details_v1, channel_messages_v1, channel_addowner_v1, channel_removeowner_v1
# from src.channels import channels_create_v1. channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1

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

'''
'users': [
        {
            'u_id': 0,
            'email': "email.com1",
            'name_first': "name_first",
            'name_last': "name_last",
            'password': "password",
            'handle_str': "namefirstlast",
            'token': 'token_str',
            'permission' ?
            'session' ?
        }
    ]  
'''

@APP.route("/auth/register/v2", methods = ['POST'])
def auth_register_http():
    register_dict = request.get_json()

    return dumps(auth_register_v2(**register_dict))

@APP.route("/auth/login/v2", methods = ['POST'])
def auth_login_http():
    login_dict = request.get_json()

    token = auth_login_v2(**login_dict)
    return dumps(token)

# @APP.route("/auth/logout/v1", methods = ['POST'])
# def auth_logout_http():
#     token = request.get_json('token')
#     auth_logout_v1(token)

#     return dumps({})

@APP.route("/channel/invite/v2", methods = ['POST'])
def channel_invite_http():
    invite_dict = request.get_json()
    channel_invite_v1(**invite_dict)
    
    return dumps({})

@APP.route("/channel/details/v2", methods = ['GET'])
def channel_details_http():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    return dumps(channel_details_v1(token, channel_id))

@APP.route("/channel/messages/v2", methods = ['GET'])
def channel_messages_http():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    return dumps(channel_messages_v1(token, channel_id, start))

@APP.route("/channel/join/v2", methods = ['POST'])
def channel_join_http():
    token = request.get_json('token')
    channel_id = int(request.get_json('channel_id'))
    channel_join_v1(token, channel_id)

    return dumps({})

# @APP.route("/channel/leave/v1", methods = ['POST'])
# def channel_leave_https():
#     token = request.get_json('token')
#     channel_id = int(request.get_json('channel_id'))
#     channel_leave_v1(token, channel_id)

#     return dumps({})

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

    return dumps(channels_list_v1(token))

@APP.route("/channels/listall/v2", methods = ['GET'])
def channels_listall_http():
    token = request.args.get('token')

    return dumps(channels_listall_v1(token))

@APP.route("/channels/create/v2", methods = ['POST'])
def channels_create_http():
    create_dict = request.get_json()

    return dumps(channels_create_v1(**create_dict))

@APP.route("/clear/v1", methods = ['DELETE'])
def clear_http():
    clear_v1()
    
    return dumps({})

# @APP.route("/message/send/v1", methods=['POST'])
# def message_send_http():
#     message_info = request.get_json()
#     token = message_info['token']
#     channel_id = int(message_info['channel_id'])
#     message = message_info['message']
#     return dumps(message_send(token, channel_id, message))

# @APP.route("/message/remove/v1", methods=['DELETE'])
# def message_remove_http():
#     message_info = request.get_json()
#     token = message_info['token']
#     message_id = int(message_info['message_id'])
#     message_remove(token, message_id)
#     return dumps({})

# @APP.route("/message/edit/v1", methods=['PUT'])
# def message_edit_http():
#     message_info = request.get_json()
#     token = message_info['token']
#     message_id = int(message_info['message_id'])
#     message = message_info['message']
#     message_edit(token, message_id, message)
#     return dumps({})

# @APP.route("/dm/create/v1", methods=['POST'])
# def dm_create_http():
#     dm_info = requests.get_json()
#     token = dm_info['token']
#     u_ids = dm_info['u_ids']
#     return dumps(dm_create_v1(token, u_ids))

# @APP.route("/dm/list/v1", methods=['GET'])
# def dm_create_http():
#     dm_info = requests.args.get()
#     token = dm_info['token']
#     return dumps(dm_list_v1(token))

# @APP.route("/dm/remove/v1", methods=['DELETE'])
# def dm_create_http():
#     dm_info = requests.get_json()
#     token = dm_info['token']
#     dm_id = dm_info['dm_id']
#     dm_remove_v1(token, dm_id)
#     return dumps({})

# @APP.route("/dm/details/v1", methods=['GET'])
# def dm_details_http():
#     dm_info = requests.args.get()
#     token = dm_info['token']
#     dm_id = dm_info['dm_id']
#     return dumps(dm_details_v1(token, dm_id))

# @APP.route("/dm/leave/v1", methods=['POST'])
# def dm_leave_http():
#     dm_info = requests.get_json()
#     token = dm_info['token']
#     dm_id = dm_info['dm_id']
#     dm_leave_v1(token, dm_id)
#     return dumps({})

# @APP.route("/message/senddm/v1", methods=['POST'])
# def message_senddm_http():
#     message_info = requests.get_json()
#     token = message_info['token']
#     dm_id = message_info['dm_id']
#     message = message_info['message']
#     return dumps(message_senddm_v1(token, dm_id, message))

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    # APP.run(port=config.port) # Do not edit this port
    APP.run(port=config.port, debug=True) # Do not edit this port

