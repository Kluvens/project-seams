# '''
# Note to self: Add some documentation here
# '''

# from src.error import InputError
# from src.auth import auth_login_v1
# from src.auth import auth_register_v1
# from src.other import clear_v1

# import pytest

# # =============================TESTING CORRECTNESS=============================

# # Test if it can the return the correct user id for an exisiting user when
# # loggin in 
# def test_login_existing_user1():
#     clear_v1()
#     email = "k123@gmail.com"
#     password = "hello12344"
#     uid = auth_register_v1(email, password, "James", "Smith")
#     return_uid = auth_login_v1(email, password)
#     assert return_uid == uid

# # Same test to the above with minor change to the email parameter
# def test_login_existing_user2():
#     clear_v1()
#     email = "k1234@gmail.com"
#     password = "hello12344"
#     uid = auth_register_v1(email, password, "James", "Smith")
#     return_uid = auth_login_v1(email, password)
#     assert return_uid == uid


# # Testing behaviour when there are a number of exisiting users in databse
# def test_login_existing_user3():
#     clear_v1()
#     auth_register_v1("k11@gmail.com", "Password123", "Casey1", "Roland")
#     auth_register_v1("k22@gmail.com", "Password123", "Casey2", "Roland")

#     email = "james123@hotmai.com"
#     password = "123james123"
#     uid = auth_register_v1(email, password, "James", "Smith")

#     auth_register_v1("k33@gmail.com", "Password123", "Casey3", "Roland")
#     auth_register_v1("k44@gmail.com", "Password123", "Casey4", "Roland")


#     return_uid = auth_login_v1(email, password)
#     assert return_uid == uid


# # ============================ TESTING EXCEPTIONS =============================

# def test_does_email_exit1():
#     clear_v1()
#     email = "k1243@gmail.com"
#     with pytest.raises(InputError):
#         auth_login_v1(email, "123123123")

# def test_does_email_exit2():
#     clear_v1()
#     email = "kaisA_13321@gmail.com"
#     with pytest.raises(InputError):
#         auth_login_v1(email, "wowowowdgdg")

# # Random incorrect password
# def test_is_password_correct1():
#     clear_v1()
#     email = "k123@gmail.com"
#     auth_register_v1(email, "ABc123HIIIIII", "John", "Smith")
#     with pytest.raises(InputError):
#         auth_login_v1(email, "HELLOHELLO123")

# # incorrect password containing the correct password as a substring
# def test_is_password_correct2():
#     clear_v1()
#     email = "k123@gmail.com"
#     auth_register_v1(email, "ABc123HIIIIII", "John", "Smith")
#     with pytest.raises(InputError):
#         auth_login_v1(email, "ABc123HIIIIIIII")

# # Incorrect password that is almost identical to the correct password
# def test_is_password_correct3():
#     clear_v1()
#     email = "k123@gmail.com"
#     auth_register_v1(email, "ABc123HIIIIII", "John", "Smith")
#     with pytest.raises(InputError):
#         auth_login_v1(email, "ABc123HIIIII")

# # Incorrect password that is identical to the correct password
# # but with lowercases only
# def test_is_password_correct4():
#     clear_v1()
#     email = "k123@gmail.com"
#     auth_register_v1(email, "ABc123HIIIIII", "John", "Smith")
#     with pytest.raises(InputError):
#         auth_login_v1(email, "abc123hiiiiii")

# # Incorrect password that is identical to the correct password but with one
# # character being lowercase instead of uppercase
# def test_is_password_correct5():
#     clear_v1()
#     email = "k123@gmail.com"
#     auth_register_v1(email, "ABc123HIIIIII", "John", "Smith")
#     with pytest.raises(InputError):
#         auth_login_v1(email, "ABc123hIIIIII")
