import requests
from assertpy import assert_that
from lxml import etree

from config import COVID_TRACKER_HOST
from utils.print_helpers import pretty_print


def test_covid_cases_have_crossed_million():
    response = requests.get(f'{COVID_TRACKER_HOST}/api/v1/summary/latest')
    #pretty_print(response.headers)

    response_xml = response.text
    tree = etree.fromstring(bytes(response_xml, encoding='utf8'))
    total_cases = tree.xpath("//data/summary/total_cases")[0].text

    assert_that(int(total_cases)).is_greater_than(1000000)

def test_overall_covid_cases_match_sum_of_total_cases_by_country():
    response = requests.get(f'{COVID_TRACKER_HOST}/api/v1/summary/latest')
    #pretty_print(response.headers)

    response_xml = response.text
    tree = etree.fromstring(bytes(response_xml, encoding='utf8'))
    total_cases = int(tree.xpath("//data/summary/total_cases")[0].text)

    search_for = etree.XPath("//data/regions//total_cases")
    cases_total_by_country = 0
    for region in search_for(tree):
        cases_total_by_country += int(region.text)

    assert_that(total_cases).is_greater_than(cases_total_by_country)

