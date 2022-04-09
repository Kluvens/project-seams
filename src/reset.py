'''
Initial desgin and implementation of auth/passwordreset/request
functionality

Kais Alzubaidi, z5246721

'''

########################## IMPORT PATHS ##########################

import uuid
import jwt
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.data_store import data_store
from src.error import InputError
from src.helpers import is_email_already_registered
from src.helpers import get_user_idx
from src.auth import is_valid_password
from src.auth import get_corresponding_user_id
from src.helpers import hash
from src.auth import auth_login_v2, auth_register_v2


##################### Caching reset_code ##########################

def cache_code(reset_code):
    with open('reset_code.txt', 'w') as fp:
        fp.write(reset_code)

    return True

####################### HELPER FUNCTIONS #########################

def logout_all_session(users, user_idx):
    for idx, user in enumerate(users):
        if idx == user_idx:
            user['sessions'] = []



def generate_reset_code(u_id):
    reset_token = uuid.uuid4().hex
    data_store.get()['reset_codes'].append(
        {
            "u_id" : u_id,
            "reset_token" : reset_token,
        }
    )

    # Storing most recent code to be used in tests
    cache_code(reset_token)

    return reset_token


def send_reset_code(email, reset_code):
    port = 465
    sender = "seams.noreply@gmail.com"
    receiver = email  
    password = "Seams12345"


    # Fomratting the email --> Convert this into HTML
    subject = "Password Reset Code"
    body = f"""Here is your requested password reset code:\n {reset_code}
     
    \n\n*************DO NOT REPLY TO THIS EMAIL***************\n\n"""

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Establishing connection and sending the email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        port,
        context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, text)


def check_can_reset_pw(reset_code, new_password):

    if not is_valid_password(new_password):
        return {
            "permission" : False,
            "reason" : "The password entered contains less than 6 characters"
        }

    codes = data_store.get()["reset_codes"]
    for code in codes:
        if code["reset_token"] == reset_code:
            u_id = code["u_id"]
            codes.remove(code)
            return {"permission" : True, "u_id": u_id}
    
    return {
    "permission" : False,
    "reason" : "The reset code you entered is invalid!"
    }


################### FUNCTION IMPLEMENTATION ######################

def auth_password_reset_request_v1(email: str) -> dict:
    '''
    This function takes in an email and creates a password reset
    request by sending a reset code to the email passsed.

    If they are email is invalid, nothing will happen

    <Argmuents>:
        - email: string
    
    <Exceptions>:
        - N/A

    <Actions>
        - A reset code will be sent to the email passed to the function
        - if the email is registered:
            - a reset_code will stored in data_store
            along with the u_id of the user that made the request.
            
            - All current sessions of the user who sent the request 
            will be logged out

    <Returns>:
        Empty Dictionary {}
    '''

    users = data_store.get()["users"]

    if is_email_already_registered(users, email):
        u_id = get_corresponding_user_id(users, email)

        user_idx = get_user_idx(users, u_id)
        logout_all_session(users, user_idx)
        reset_code = generate_reset_code(u_id)
        send_reset_code(email, reset_code)

    return {}



def auth_password_reset_v1(reset_code: str, new_password: str) -> dict:
    '''
    This function takes in a reset code string and a password string.
    If they are both valid, the user's password is reset to the new
    password.

    <Argmuents>:
        - reset_code: string.
        - new_password: string.
    
    <Exceptions>:
        - InputError:
            1) Raised when reset_code is not a valid reset code.
            2) Raised when length of new_password is less than 6 characters.
    
    <Actions>
        - If not expcetions are raised, the user's who sent the reset_code
        will have their password reset as new_password.
        - The reset_code will be invalidated 
    
    <Returns>:
        Empty Dictionary {}
    '''

    response = check_can_reset_pw(reset_code, new_password)
    if response["permission"]:
        u_id = response["u_id"]
        users = data_store.get()["users"]
        user_idx = get_user_idx(users, u_id)
        users[user_idx]["password"] = hash(new_password)
    else:
        raise InputError(description=response["reason"])

    return {}


################## END OF FUNCTION IMPLEMENTATION ################

if __name__ == "__main__":
    email = "seams.noreply@gmail.com"
    u0 = auth_register_v2(email, "password", "Kai", "Kakarot")
    auth_login_v2(email, "password")
    auth_login_v2(email, "password")
    auth_login_v2(email, "password")
    auth_login_v2(email, "password")

    data = data_store.get()
    users = data["users"]
    reset_codes = data["reset_codes"]
    
    print(users)

    print(reset_codes)
    print("\n\n")


    auth_password_reset_request_v1(email)    
    print(reset_codes)
    print("\n\n\n\n")
    
    auth_password_reset_v1(token, "123123123")

    print(reset_codes)
    print("\n\n\n\n")

    print(users)

    # auth_login_v2(email, "password")
    auth_login_v2(email, "123123123")

    print(users)
