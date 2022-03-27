# Iteration 1:

27/2/2022 - 7pm/8:30pm


•	Need to write a standard data struct
•	James: Have implemented test cases, not sure about data struct 
•	Ryan: Haven’t really started, busy, will finish by tomorrow or tonight
•	Jazzy: Test for channel join done, wanted to check in about other things before continuing to write
•	Kais: ** couldn’t hear well, implemented some stuff out of spec??
•	Justin: Did some tests and function stuff, worried about inconsistencies so didn’t continue
•	Sort out data structure system
•	Using standard data_store.py given in spec until later iterations
•	Tuesday night meeting 8:15pm: finish all tests, hopefully functions 
•	Jazzy to make a server 

1/3/2022 - 8:15/9pm


•	Need to push data struct branch so we can all pull from it
•	Not sure where messages are generated, will go to help session to check if we need to write another function or if there is something else to do

3/3/2022 - 9pm
•	·Changed the datastore structure’s variable naming
o	 uid -> u_id
o	cid -> channel_id
•	·merge requests to be made merging our branches between each other than merging to master at a later date
•	·         created a table of dependencies
•	·         code review of Kais code
•	·         code review of james_listall code


# Iteration 2:
20/3/2022 – 9pm
•	Allocated tasks and had a read through of iteration 2 to ensure understanding of the project
•	Allocated goals for next meeting including the basic implementation of v2 functions from iteration1 and basic testing
•	Fixed issues in iteration 1 project
22/3/2022 – 9pm
•	Code reviews of every member’s code made including reconsolidating our understanding of http testing
•	Assigned goals of converting current black box tests to http tests
•	Started creation and discussion of new data structure including DMs and made minor changes to data structure
24/3/2022 – 9pm
•	Code reviews of each member’s progress made which included newly written http tests and v2 implementations of iteration1 functions
•	Created new data structure including DMs
25/3/2022 – 9pm
•	Allocated goals for weekend including the implementation of iteration2 functions and basic http testing
•	James and Kais: Started creation of dm_create
•	Merge requests by Kais and James made to master
•	Debugging of list http tests
26/3/2022 – 9pm
•	Debugging of channel_create and channel_list/listall complete. Changes were made to server.py and names of keys and http tests.
•	James: Completed implementation and testing of list/listall functions including finishing off dm_create. Dm_list and and dm_details testing completed
•	Ryan: Basic implementation of messages completed with failing tests
•	Jiapeng: Completed respective channels functions and testing
•	Kais: Completed auth functions and testing, working through user functions and testing
•	Jasmine: Completed basic testing of channels funcs and dms

27/3/2022 – 9pm
•	More debugging worked through and solved
•	Completed full implementations and http testing on functions.
•	Coordinated merge requests
•	Pylint fixes, added docstrings
•	Changed syntax of http testing code including adding OKAY = 200 and AccessError.code and InputError.code
•	Coverage testing
•	Organised server.py
•	Organised helper functions into helper.py and http_helpers.py
