# Tests for functions which communicate with BOINC. These will obviously fail if BOINC is not open.
import pytest

import config
import main
import libs.pyboinc
rpc_user=None
rpc_port=None
rpc_password=None
CONNECTION_OBJECT:main.BoincClientConnection=None
RPC_CONNECTION_OBJECT:libs.pyboinc.rpc_client.RPCClient=None

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
def test_setup_connection():
    global RPC_CONNECTION_OBJECT
    RPC_CONNECTION_OBJECT=main.setup_connection(config.boinc_ip,config.boinc_password,config.boinc_port)
    assert isinstance(RPC_CONNECTION_OBJECT,libs.pyboinc.rpc_client.RPCClient)
