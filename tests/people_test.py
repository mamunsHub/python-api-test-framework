from json import dumps
from config import BASE_URI
from assertpy.assertpy import assert_that
from utils.print_helpers import pretty_print
from uuid import uuid4

import requests


def test_read_all_data():
    peoples, response = get_all_users()
    # response from requests has many useful properties
    # we can assert on the response status code    
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    # pretty_print(peoples)

    # now validate data 
    # validating a first name of a user call kent
    first_names = [people['fname'] for people in peoples]
    assert_that(first_names).contains('Kent')



def test_new_person_can_be_added():
    unique_last_name = create_new_person()

    # Check if new person is added successfully
    peoples = requests.get(BASE_URI).json()
    new_users = search_users_by_last_name(peoples, unique_last_name)
    assert_that(new_users).is_not_empty()




def test_new_person_can_be_deleted():
    new_user_last_name = create_new_person()
    all_users, _ = get_all_users() # it fetches only the first returned variable from the function
    new_user = search_users_by_last_name(all_users, new_user_last_name)[0]

    #print(new_user)
    person_to_be_deleted = new_user['person_id']  # Fetching id of the newly created user
    url = f'{BASE_URI}/{person_to_be_deleted}'
    responses = requests.delete(url)
    assert_that(responses.status_code).is_equal_to(200)
    assert_that(responses.status_code).is_equal_to(requests.codes.ok)

    # validate if deleted user can not be found
    all_new_users, _ = get_all_users()
    user_ids = [people['person_id'] for people in all_new_users]
    assert_that(user_ids).does_not_contain(person_to_be_deleted)



def get_all_users():
    # We use requests.get() with url to make a get request
    # We can get python dict as response by using .json() method
    response = requests.get(BASE_URI)
    peoples = response.json()
    return peoples, response


def create_new_person():
    # Creating new person with unique last name every time the test is executed
    # Note: json.dumps() is used to convert python string to json string
    unique_last_name = f'User {str(uuid4())}'
    payload = dumps({
        'fname': 'New',
        'lname': unique_last_name
    })

    # Headers setup with json and content-type
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    # requests.post method with keyword params is used to make the request
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(204)
    return unique_last_name



def search_users_by_last_name(peoples, unique_last_name):
    return [person for person in peoples if person['lname'] == unique_last_name]