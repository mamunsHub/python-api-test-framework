from json import dumps
from config import BASE_URI
from assertpy.assertpy import assert_that, soft_assertions
from utils.print_helpers import pretty_print
from uuid import uuid4

import requests


def test_read_all_data():
    peoples, response = get_all_users()
    # response from requests has many useful properties
    # we can assert on the response status code
    with soft_assertions():
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        # pretty_print(peoples)

        # now validate data
        # validating a first name of a user call kent
        #first_names = [people['fname'] for people in peoples]
        assert_that(peoples).extracting('fname').is_not_empty().contains('Kent')  # fluent assertions


def test_new_person_can_be_added():
    unique_last_name = create_new_person()

    # Check if new person is added successfully
    peoples = requests.get(BASE_URI).json()
    new_users = search_users_by_last_name(peoples, unique_last_name)
    with soft_assertions():
        assert_that(new_users).is_not_empty()


def test_person_info_can_be_updated():
    new_user_last_name = create_new_person()
    all_users, _ = get_all_users()
    # check if people with same name exists
    user = search_users_by_last_name(all_users, 'Abdullah')[0]
    user_id = user['person_id']
    if user_id > 0:
        url = f'{BASE_URI}/{user_id}'
        responses = requests.delete(url)   # if exists then the data will be deleted to exclude conflict

    new_user = search_users_by_last_name(all_users, new_user_last_name)[0]
    new_user_id = new_user['person_id']
    #print(new_user_id)

    # Data to update
    payload = dumps({
        'fname': 'Mamun',

        'lname': 'Abdullah'
    })

    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    # Making put request to update the data
    url = f'{BASE_URI}/{new_user_id}'
    response = requests.put(url=url, data=payload, headers=headers)
    #print(response)

    with soft_assertions():
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.status_code).is_equal_to(requests.codes.ok)

        # validate if user is updated
        all_new_users, _ = get_all_users()
        # check if update people with new name exists
        assert_that(all_new_users).extracting('fname').contains('Mamun')
        assert_that(all_new_users).extracting('lname').contains('Abdullah')
        assert_that(all_new_users).extracting('person_id').contains(new_user_id)


def test_new_person_can_be_deleted():
    new_user_last_name = create_new_person()
    all_users, _ = get_all_users()  # it fetches only the first returned variable from the function
    new_user = search_users_by_last_name(all_users, new_user_last_name)[0]

    # print(new_user)
    person_to_be_deleted = new_user['person_id']  # Fetching id of the newly created user
    url = f'{BASE_URI}/{person_to_be_deleted}'
    responses = requests.delete(url)

    with soft_assertions():
        assert_that(responses.status_code).is_equal_to(200)
        assert_that(responses.status_code).is_equal_to(requests.codes.ok)

        # validate if deleted user can not be found
        all_new_users, _ = get_all_users()
        #user_ids = [people['person_id'] for people in all_new_users]
        assert_that(all_new_users).extracting('person_id').does_not_contain(person_to_be_deleted)


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
