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
