# '''
# This is an additional testing module for the auth_register_v1 function.
# These tests here adhere to the blackbox testing method.

# '''

# from src.auth import auth_register_v1
# from src.channels import channels_create_v1
# from src.channel import channel_details_v1
# from src.channel import channel_invite_v1
# from src.other import clear_v1


# #===================== Testing Correctness =======================

# # ======================== SET 1 =================================
# # Concatenation of first name and last name is less than or or
# # equal to 20 characters.
# # Handle is unique (not taken by an existing user)


# # First and last names strictly contain lowercase characters.
# def test_simple_handle1():
#     clear_v1()

#     uid_dict = auth_register_v1(
#             "k.z123@gmail.com",
#             "a1b2c3d4e5",
#             "kais",
#             "alzubaidi")

#     u_id = uid_dict['auth_user_id']

#     # channel_create_v1 takes in a boolean is_public parameter
#     c_id = channels_create_v1(u_id, "channel0", True)['channel_id']

#     owner_members_list = channel_details_v1(u_id, c_id)['owner_members']

#     # No need for a search since only one user exist
#     user_handle_str = owner_members_list[0]['handle_str']

#     assert user_handle_str == "kaisalzubaidi"


# #First and last names contain uppercase characters
# def test_simple_handle2():
#     clear_v1()

#     uid_dict = auth_register_v1(
#             "k.z123@gmail.com",
#             "a1b2c3d4e5",
#             "KaIS",
#             "AlzuBaidI")

#     u_id = uid_dict['auth_user_id']

#     # channel_create_v1 takes in a boolean is_public parameter
#     c_id = channels_create_v1(u_id, "channel0", True)['channel_id']

#     owner_members_list = channel_details_v1(u_id, c_id)['owner_members']

#     user_handle_str = owner_members_list[0]['handle_str']

#     assert user_handle_str == "kaisalzubaidi"


# # First and last names contain a mix of alphanumeric characters
# def test_simple_handle3():
#     clear_v1()

#     uid_dict = auth_register_v1(
#             "k.z123@gmail.com",
#             "a1b2c3d4e5",
#             "KaIS12",
#             "AlzuBaidI92190")

#     u_id = uid_dict['auth_user_id']

#     # channel_create_v1 takes in a boolean is_public parameter
#     c_id = channels_create_v1(u_id, "channel0", True)['channel_id']

#     owner_members_list = channel_details_v1(u_id, c_id)['owner_members']

#     user_handle_str = owner_members_list[0]['handle_str']

#     assert user_handle_str == "kais12alzubaidi92190"



# # Shortest valid first and last name handle generation
# def test_simple_handle4():
#     clear_v1()

#     uid_dict = auth_register_v1("k.z123@gmail.com", "a1b2c3d4e5", "K", "z")

#     u_id = uid_dict['auth_user_id']

#     # channel_create_v1 takes in a boolean is_public parameter
#     c_id = channels_create_v1(u_id, "channel0", True)['channel_id']

#     owner_members_list = channel_details_v1(u_id, c_id)['owner_members']

#     user_handle_str = owner_members_list[0]['handle_str']

#     assert user_handle_str == "kz"


# # ======================== SET 2 =================================
# # Test behaviour for long names
# # Concatenated string of first and last name exceeds 20 characters


# # Testing handle generation for long user name that does not contain numbers
# def test_long_username_handle1():
#     clear_v1()

#     uid_dict = auth_register_v1(
#             "i_hate_tests123@gmail.com",
#             "wowhisnameislong123",
#             "Hubert",
#             "Wolfeschlegelsteinhausenbergredroff")

#     u_id = uid_dict['auth_user_id']

#     # channel_create_v1 takes in a boolean is_public parameter
#     c_id = channels_create_v1(u_id, "channel0", True)['channel_id']

#     owner_members_list = channel_details_v1(u_id, c_id)['owner_members']

#     user_handle_str = owner_members_list[0]['handle_str']

#     assert user_handle_str == "hubertwolfeschlegels"

# # Testing handle generation for long user name that
# # contains a mix of alphanumeric characters
# def test_long_username_handle2():
#     clear_v1()

#     uid_dict = auth_register_v1(
#             "kakarot999@gmail.com",
#             "powerlevelover9000",
#             "SonGuko",
#             "SuperSayianGodSuperSayianKaioKenX20")


#     u_id = uid_dict['auth_user_id']

#     # channel_create_v1 takes in a boolean is_public parameter
#     c_id = channels_create_v1(u_id, "channel0", False)['channel_id']

#     owner_members_list = channel_details_v1(u_id, c_id)['owner_members']

#     user_handle_str = owner_members_list[0]['handle_str']


#     user_handle_str = owner_members_list[0]['handle_str']
#     assert user_handle_str == "songukosupersayiango"


# # ======================== SET 3 =================================
# # Test behaviour if handle is taken with simple names


# # Searching for u_id or assume they are added in order?

# # Test behaviour if handle is taken and require an incrementing suffix
# def test_taken_handle_simple1():
#     clear_v1()

#     uid1_dict = auth_register_v1(
#             "k.z123@gmail.com",
#             "a1b2c3d4e5",
#             "kais",
#             "alzubaidi")

#     u_id1 = uid1_dict['auth_user_id']

#     uid2_dict = auth_register_v1(
#             "k.z1234@gmail.com",
#             "a1b2c3d4e5",
#             "kais",
#             "Al_zubaidi")

#     u_id2 = uid2_dict['auth_user_id']


#     channel_id_dict = channels_create_v1(u_id1, "channel0", True)
#     c_id = channel_id_dict['channel_id']

#     channel_invite_v1(u_id1, c_id, u_id2)

#     channel_dict = channel_details_v1(u_id1, c_id)
#     members_list = channel_dict['all_members']



#     user1_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id1 == user['u_id']
#     ]

#     user2_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id2 == user['u_id']
#     ]

#     # [0] because we used lists comprehension so we have a list
#     # with one element which is the handle string
#     assert user1_handle_str[0] == "kaisalzubaidi"
#     assert user2_handle_str[0] == "kaisalzubaidi0"


# # Test handle generation for multiple users where the concatenation
# # of their first and last names matches existing users.
# # Once users are registers, we will check if the appropriate uid
# def test_taken_handle_simple2():
#     clear_v1()

#     uid1_dict = auth_register_v1(
#             "k.z123@gmail.com",
#             "a1b2c3d4e5",
#             "kais",
#             "alzubaidi")

#     u_id1 = uid1_dict['auth_user_id']

#     uid2_dict = auth_register_v1(
#             "k.z1234@gmail.com",
#             "a1b2c3d4e5",
#             "kais",
#             "Al_zubaidi")

#     u_id2 = uid2_dict['auth_user_id']

#     uid3_dict = auth_register_v1(
#             "k.z123456@gmail.com",
#             "a1b2c3d4e5",
#             "KAIS",
#             "ALZUBAIDI")

#     u_id3 = uid3_dict['auth_user_id']

#     uid4_dict = auth_register_v1(
#             "k.z1234567@gmail.com",
#             "a1b2c3d4e5",
#             "kais",
#             "ALZubaidi")

#     u_id4 = uid4_dict['auth_user_id']

#     channel_id_dict = channels_create_v1(u_id1, "channel0", True)
#     c_id = channel_id_dict['channel_id']

#     channel_invite_v1(u_id1, c_id, u_id2)
#     channel_invite_v1(u_id1, c_id, u_id3)
#     channel_invite_v1(u_id1, c_id, u_id4)

#     channel_dict = channel_details_v1(u_id1, c_id)
#     members_list = channel_dict['all_members']


#     user1_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id1 == user['u_id']
#     ]

#     user2_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id2 == user['u_id']
#     ]

#     user3_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id3 == user['u_id']
#     ]

#     user4_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id4 == user['u_id']
#     ]

#     # [0] because we used lists comprehension so we have a list
#     # with one element which is the handle string
#     assert user1_handle_str[0] == "kaisalzubaidi"
#     assert user2_handle_str[0] == "kaisalzubaidi0"
#     assert user3_handle_str[0] == "kaisalzubaidi1"
#     assert user4_handle_str[0] == "kaisalzubaidi2"



# # Test behaviour if handle is taken with long names, when handle generation
# # requires adding an incrementing interger suffix at the end
# # (which may exceed 20 characters)
# def test_taken_handle_long1():
#     clear_v1()

#     uid1_dict = auth_register_v1(
#             "i_hate_tests123@gmail.com",
#             "a1b2c3d4e5",
#             "Hubert",
#             "Wolfeschlegelsteinhausenbergredroff123345dsfa")

#     u_id1 = uid1_dict['auth_user_id']

#     uid2_dict = auth_register_v1(
#             "i_hate_tests1234@gmail.com",
#             "a1b2c3d4e5",
#             "Hubert__",
#             "Wolfeschlegelste12")

#     u_id2 = uid2_dict['auth_user_id']

#     uid3_dict = auth_register_v1(
#             "i_hate_tests12345@gmail.com",
#             "a1b2c3d4e5",
#             "__HuBert___",
#             "Wolfeschlegelsteinhause34235nbergr")

#     u_id3 = uid3_dict['auth_user_id']

#     channel_id_dict = channels_create_v1(u_id1, "channel0", True)
#     c_id = channel_id_dict['channel_id']

#     channel_invite_v1(u_id1, c_id, u_id2)
#     channel_invite_v1(u_id1, c_id, u_id3)

#     channel_dict = channel_details_v1(u_id1, c_id)
#     members_list = channel_dict['all_members']


#     user1_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id1 == user['u_id']
#     ]

#     user2_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id2 == user['u_id']
#     ]

#     user3_handle_str = [
#         user['handle_str'] for user in members_list
#         if u_id3 == user['u_id']
#     ]

#     assert user1_handle_str[0] == "hubertwolfeschlegels"
#     assert user2_handle_str[0] == "hubertwolfeschlegels0"
#     assert user3_handle_str[0] == "hubertwolfeschlegels1"
