# Tests for functions which communicate with BOINC. These will obviously fail if BOINC is not open.
import pytest
import main
rpc_user=None
rpc_port=None
rpc_password=None
CONNECTION_OBJECT:main.BoincClientConnection=None

BOINC_DATA_DIR=main.BOINC_DATA_DIR
@pytest.fixture
def test_BoincClientConnection():
    global CONNECTION_OBJECT
    CONNECTION_OBJECT = main.BoincClientConnection(config_dir=BOINC_DATA_DIR)
    assert CONNECTION_OBJECT
def test_BoincClientConnection_get_project_list(test_BoincClientConnection):
    project_list=CONNECTION_OBJECT.get_project_list()
    assert isinstance(project_list,list)
    assert len(project_list)>3