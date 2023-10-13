import pytest
import main
from typing import Dict,List,Tuple,Union,Any
# Tests that require a network connection and will fail without one
APPROVED_PROJECT_URLS={}
@pytest.fixture()
def test_get_approved_project_urls_web():
    """
    This test only tests network functionality. Test of parsing etc is found in a similar test in main tests
    @return:
    """
    global APPROVED_PROJECT_URLS
    APPROVED_PROJECT_URLS=main.get_approved_project_urls_web()
def test_get_project_mag_ratios_from_url(test_get_approved_project_urls_web):
    result=main.get_project_mag_ratios_from_url(30,APPROVED_PROJECT_URLS)
    assert len(result)>3
def test_get_grc_price_regex():
    # Function to test the regexes for getting grc price. Note this may fail if you get a "are you a bot?" page.
    # Inspect HTML before assuming the regex is broken
    import requests as req
    import re
    headers = req.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    })

    sample_text=None
    for url, info in main.PRICE_URL_DICT.items():
        regex = info[1]
        name = info[0]
        resp = ''
        if sample_text:
            resp = sample_text
        else:
            resp = req.get(url, headers=headers).text
        regex_result = re.search(regex, resp)
        assert regex_result
        float(regex_result.group(2))
def test_grc_grc_price():
    answer=main.get_grc_price()
    assert isinstance(answer,float)