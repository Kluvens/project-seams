# import pytest

# from src.channels import channels_list_v2, channels_create_v1
# from src.other import clear_v1
# from src.error import AccessError
# from src.auth import auth_register_v1

# # =============================TESTING CORRECTNESS============================

# # test if list func doesn't return dict when inputting user_id with
# # non-existant channel public and private
# def test_no_channels_joined_private():
#     clear_v1()

#     # create two users
#     u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
#     u_id2 = auth_register_v1("e2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create private channel for user 1
    # channels_create_v1(u_id1['token'], "ch1", False)

    # return channels for user 2 (non-existant)
    # listv1 = channels_list_v2(u_id2['token'])
    
#     assert listv1 == {'channels': []}

# def test_no_channels_joined_public():
#     clear_v1()

#     # create two users
#     u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
#     u_id2 = auth_register_v1("e2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create public channel for user 1
    # channels_create_v1(u_id1['token'], "ch1", True)

    # return channels for user 2 (non-existant)
    # listv1 = channels_list_v2(u_id2['token'])

#     # pass if trying to access non-existant channel 
#     assert listv1 == {'channels': []}   

# # test func output when user has joined all channels public and private
# def test_user_join_all_channels_private():
#     clear_v1()

#     # create user
#     u_id1 = auth_register_v1("james@gmail.com", "abcdefg123", "James", "Cai")
#     auth_register_v1("james2@gmail.com", "abcdefg123", "Jam", "Cao")

    # create channels
    # ch1 = channels_create_v1(u_id1['token'], "ch1", False)
    # ch2 = channels_create_v1(u_id1['token'], "ch2", False)

    # listv1 = channels_list_v2(u_id1['token'])

#     # assert user 1 is part of all channels
#     assert listv1['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'},
#                                 {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

# def test_user_join_all_channels_public():
#     clear_v1()

#     # create user
#     u_id1 = auth_register_v1("james@gmail.com", "abcdefg123", "James", "Cai")
#     auth_register_v1("james2@gmail.com", "abcdefg123", "Jam", "Cao")

#     # create channels
#     ch1 = channels_create_v1(u_id1['auth_user_id'], "ch1", True)
#     ch2 = channels_create_v1(u_id1['auth_user_id'], "ch2", True)

#     listv1 = channels_list_v1(u_id1['auth_user_id'])

#     # assert user 1 is part of all channels
#     assert listv1['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'}, 
#                                 {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

# # test func output when user has joined some channels public and private
# def test_user_join_some_channels_private():
#     clear_v1()

#     # create users
#     u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
#     u_id2 = auth_register_v1("e2@gmail.com", "abcdefg1234", "Jam", "Cao")

#     # create channels with u_id1 as owner of ch1 and ch2 and not a member
#     # of ch3
#     ch1 = channels_create_v1(u_id1['auth_user_id'], "ch1", False)
#     ch2 = channels_create_v1(u_id1['auth_user_id'], "ch2", False)
#     channels_create_v1(u_id2['auth_user_id'], "ch3", False)

#     listv1 = channels_list_v1(u_id1['auth_user_id'])

#     # assert user 1 is part of ch1 and ch2
#     assert listv1['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'}, 
#                                 {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

# def test_user_join_some_channels_public():
#     clear_v1()

#     # create users
#     u_id1 = auth_register_v1("e1@gmail.com", "abcdefg123", "James", "Cai")
#     u_id2 = auth_register_v1("e2@gmail.com", "abcdefg1234", "Jam", "Cao")

#     # create channels with u_id1 as owner of ch1 and ch2 and not a member
#     # of ch3
#     ch1 = channels_create_v1(u_id1['auth_user_id'], "ch1", True)
#     ch2 = channels_create_v1(u_id1['auth_user_id'], "ch2", True)
#     channels_create_v1(u_id2['auth_user_id'], "ch3", True)

#     listv1 = channels_list_v1(u_id1['auth_user_id'])

#     # assert user 1 is part of ch1 and ch2
#     assert listv1['channels'] == [{'channel_id': ch1['channel_id'], 'name': 'ch1'}, 
#                                 {'channel_id': ch2['channel_id'], 'name': 'ch2'}]

# # =============================TESTING ERRORS================================

# def test_invalid_input_string():
#     clear_v1()
#     with pytest.raises(AccessError):
#         channels_list_v1('BOBbob')

# def test_invalid_input_invalid_user_id():
#     clear_v1()
#     with pytest.raises(AccessError):
#         channels_list_v1(10)

