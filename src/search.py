'''
This module contains the implementaiton of the
search route functionality.

Almost complete ===== Require react and pin to test 

Kais Alzubaidi, z524621

'''
####################### Import Statements ########################
from src.error import AccessError
from src.error import InputError
from src.data_store import data_store
from src.helpers import check_if_token_exists
from src.helpers import decode_token


################## paths for white box tests #################
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.message import message_send_v1
from src.channel import channel_invite_v2


###################### Helper functions ##########################

def get_all_members_u_ids(all_members: list) -> list:
    memeber_u_ids = [member["u_id"] for member in all_members]
    return memeber_u_ids


def find_target_message(messages_list: list, query_str, u_id) -> dict:
    not_found = {"found" : False} 
    if not messages_list:
        return not_found

    target_messages_indicies = []
    for idx, message_dict in enumerate(messages_list):
        if query_str.lower() in message_dict["message"].lower():
            target_messages_indicies.append(idx)
            # return {"found" : True, "message_dict" : message_dict}
    if target_messages_indicies:
        return {"found" : True, "messages_indicies" : target_messages_indicies}

    return not_found


def filter_messages(target_messages, u_id):
    filtered_list = []
    for message_dict in target_messages:
        filtered_list.append(
            {
                "message_id" : message_dict["message_id"],
                "u_id" : message_dict["u_id"],
                "message" : message_dict["message"],
                "time_sent" : message_dict["time_sent"]
            }
        )
        # Check if is_pinned key exists
        if "is_pinned" in message_dict:
            filtered_list[-1].update(
                {"is_pinned" : message_dict["is_pinned"]})
        else:
            filtered_list[-1]["is_pinned"] = False

        # Check if reacts key exits
        # change this to a list comprehension
        if "reacts" in message_dict and message_dict["reacts"]: 
            reacts_output = []
            reacts = message_dict["reacts"]
            for react in reacts:
                reacts_output.append(extract_react_dict(react, u_id))
            filtered_list[-1].update(
                {"reacts" : reacts_output})
        else:
            filtered_list[-1]["reacts"] = []

    return filtered_list

def get_target_messages(messages_list, target_messages_indicies):
    target_messages = []
    for idx in target_messages_indicies:
        target_messages.append(messages_list[idx])
    return target_messages


def extract_react_dict(react, u_id):
    return {
            "react_id" : react["react_id"],
            "u_ids" : react["u_ids"],
            "is_this_user_reacted" : is_user_reacted(react["u_ids"], u_id)
            }


def is_user_reacted(u_ids, u_id):
    if not u_ids:
        return False
    if u_id in u_ids:
        return True
    return False

#def get_filtered_messages()


###################### Function Implementations ###################

# What if the user hasnt joined any channel will message be empty
def search_v1(token: str, query_str: str) -> dict:
    '''
    <<Description>>
    Given a query string, return a collection of messages in all 
    of the channels/DMs that the user has joined that 
    contain the query (case-insensitive). 
    There is no expected order for these messages.

    <<Arguments>>
        - token: str
        - query_str: str
    
    <<Exceptions>>
        - AccessError: 
            - Occurs when an invalid token is passed in.
        - InputError:
            - Occurs when the length of query_str is less than or
            greater than 1000 characters.

    <<Retrun>>
        - {"messages" : messages}
        where messages is a dict List of dictionaries, 
        where each dictionary contains types 
        { message_id, u_id, message, time_sent, reacts, is_pinned } 

    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token!!")
    
    if not (1 <= len(query_str) <= 1000):
        raise InputError(
            description="Query string must be between 1 and 1000 characters.")

    u_id = decode_token(token)
    channels = data_store.get()["channels"]
    target_messages = []
    for channel in channels:
        if u_id in get_all_members_u_ids(channel["all_members"]):
            target = find_target_message(
                channel["messages"], query_str, u_id)
            if target["found"]:
                target_messages = get_target_messages(
                    channel["messages"], target["messages_indicies"])

    
    if not target_messages:
        return_msg_list = target_messages
    else:
        return_msg_list = filter_messages(target_messages, u_id)


    dms = data_store.get()["dms"]
    target_dms = []
    for dm in dms:
        if u_id in get_all_members_u_ids(dm["all_members"]):
            target = find_target_message(
                dm["messages"], query_str, u_id)
            if target["found"]:
                target_dms = get_target_messages(
                    dm["messages"], target["messages_indicies"])
    
    if not target_dms:
        return_dm_list = target_dms
    else:
        return_dm_list = filter_messages(target_dms, u_id)

    return {"messages" : (return_msg_list + return_dm_list)}

    
################## END OF FUNCTION IMPLEMENTATION ################
