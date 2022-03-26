from src.data_store import data_store
from src.error import AccessError
from src.error import InputError
from src.helpers import check_if_token_exists
from src.helpers import decode_token
from src.helpers import generate_handle
from src.helpers import is_valid_name
from src.helpers import is_valid_email
from src.helpers import is_email_already_registered
from src.helpers import check_handlestr_unique
from src.helpers import get_user_idx




# Can any user request this function
# def user_all_v1(token):
#     '''
#     This function displays all the user details
#     that are registered in the database

#     Arguments: token, type: str
    
#     Exceptions: 
#         - Throws an AccessError when an invalid token
#         string is passed
    
#     Return: A list of user dictionaries, where
#     each dict has a key-value pair of
#     u_id, email, name_first, name_last, handle_str

#     '''
#     if not check_if_token_exists(token):
#         raise AccessError(description="Invalid Token")

#     users = data_store.get()["users"]
#     users_details = []
#     for user in users:
#         users_details.append({
#             "u_id" : user["u_id"],
#             "email" : user["email"],
#             "name_first": user["name_first"],
#             "name_last" : user["name_last"],
#             "handle_str" : user["handle_str"]
#         })

#     return users_details


# Can any user request this function
def user_profile_v1(token, u_id):
    
    # u_id = int(u_id)
    '''
    This function displays all the user details
    that belong to the u_id passed to the function

    Arguments: 
        - token, type: str
        - u_id, type: int 
    
    Exceptions: 
        - Throws an AccessError when an invalid token
        string is passed
        - Throws an AccessError when an invalid u_id
        is passed
    
    Return: A dictionary that has the follwing keys
    and their corresponding values:
    u_id, email, name_first, name_last, handle_str
    '''
    if not check_if_token_exists(token):
        raise AccessError(description="Invalid Token")
        
    users = data_store.get()["users"]

    if get_user_idx(users, u_id) is None:
        raise AccessError(
            description="This u_id does not belong to a valid user")

    user_profile = {}
    for user in users:
        if u_id == user["u_id"]:
            user_profile = {
                "u_id" : u_id,
                "email" : user["email"],
                "name_first": user["name_first"],
                "name_last" : user["name_last"],
                "handle_str" : user["handle_str"]
            }

    return user_profile
