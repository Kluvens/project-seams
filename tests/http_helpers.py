import json
import requests
from src.helpers import hash
from src.config import url


def reset_call():
    requests.delete(url + 'clear/v1')

class GenerateTestData:
    '''
    This class generates dummy user data.
    
    For example, when testing the auth/register/v2
    route, we will need to pass in pass in some data
    in the request body, and receive some data in return

    By calling the register_users() method of this class, 
    and giving it the number of users we would like to register,
    it will automate the process for us by sending n requests, whereby
    n unique users will be registered and the return for each request
    will be added to a list of dictionaries that will eventually be returned

    Note that this should not violate the blackbox testing method,
    as we are only calling the routes, passing them some data
    and only returning the data that a given request has returned.

    I have defined additional methods to allow for flexibile use
    of this class by other developers.
    '''

    def __init__(self, url):
        self.url = url
    
    def data_owner(self):
        return {
            "email" : "owner@seams.com",
            "password" : "Iamanowner123",
            "name_first" : "Jake",
            "name_last" : "Renzella"
        }


    def data_dummy1(self):
        return {
            "email" : "dummy1@seams.com",
            "password" : "dummy1_123",
            "name_first" : "testfirst1",
            "name_last" : "testlast1"
        }


    def data_dummy2(self):
        return  {
            "email" : "dummy2@seams.com",
            "password" : "dummy2_123",
            "name_first" : "testfirst2",
            "name_last" : "testlast2"
        }

    def data_dummy3(self):
        return {
            "email" : "dummy3@seams.com",
            "password" : "dummy3_123",
            "name_first" : "testfirst3",
            "name_last" : "testlast3"
        }


    

    def dummy_channel0(self, token):
        return {
            "token" : str(token),
            "name" : "DummyChannel0",
            "is_public" : True
        }


    def dummy_channel1(self, token):
        return {
            "token" : str(token),
            "name" : "DummyChannel1",
            "is_public" : False
        }


    def dummy_users_data(self, num_of_users):
        dummy_users = {
            0 : self.data_owner,
            1 : self.data_dummy1,
            2 : self.data_dummy2,
            3 : self.data_dummy3
        }

        # list of dictionaries
        users_info = []
        for user_num in dummy_users:
            if user_num > num_of_users - 1:
                break
            else:
                users_info.append(dummy_users[user_num]())

        return users_info



    def register_users(self, num_of_users):
        '''
        '''
        users = self.dummy_users_data(num_of_users)
        register_user_route = self.url + 'auth/register/v2'
        registered_users = [] 
        for user in users:
            user_reg_info = requests.post( 
                register_user_route,
                json=user
            )
            user_dict = user_reg_info.json()
            registered_users.append(user_dict)
        
        return registered_users


    def login(self, num_of_users):
        '''
        '''
        users = self.dummy_users_data(num_of_users)
        register_user_route = self.url + 'auth/login/v2'
        logged_in_users = [] 
        for idx in range(len(users)):
            user_login_info = requests.post( 
                register_user_route,
                json={"email" : users[idx]["email"], 
                "password" : users[idx]["password"]}
            )
            user_dict = user_login_info.json()
            logged_in_users.append(user_dict)
        
        return logged_in_users


    def logout_request(self, token):
        '''
        '''
        # print(token)
        route = self.url + 'auth/logout/v1'
        response = requests.post(route, json={"token" : token})
        assert response.status_code == 200
    

    # for now this supports up to 2 channels
    def create_channel(self, num_of_channels, token):
        '''
        '''
        parameters = self.dummy_channel0(token)
        route = self.url + '/channels/create/v2'
        response = requests.post(
            route,
            json=parameters
        )
        return response
