import requests

from config import BASE_URI
from assertpy.assertpy import assert_that
from utils.print_helpers import pretty_print


def test_read_all_data():
    # We use requests.get() with url to make a get request
    response = requests.get(BASE_URI)
    # response from requests has many useful properties
    # we can assert on the response status code    
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    # We can get python dict as response by using .json() method
    peoples = response.json()
    #pretty_print(peoples)

    # now validate data 
    # validating a first name of an user call kent
    first_names = [people['fname'] for people in peoples]
    assert_that(first_names).contains('Kent')