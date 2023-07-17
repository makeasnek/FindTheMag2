# Tests for functions which communicate with Gridcoin wallet. These will obviously fail if wallet is not online.
# These tests will also fail if there is no user/pass/port in your gridcoin.conf
import pytest
import main
rpc_user=None
rpc_port=None
rpc_password=None
connection_object:main.GridcoinClientConnection=None
@pytest.fixture
def test_get_gridcoin_config_parameters():
    global rpc_user
    global rpc_password
    global rpc_port
    gridcoin_data_dir=main.GRIDCOIN_DATA_DIR
    gridcoin_conf = main.get_gridcoin_config_parameters(gridcoin_data_dir)
    assert gridcoin_conf
    rpc_user = gridcoin_conf.get('rpcuser')
    rpc_password = gridcoin_conf.get('rpcpassword')
    rpc_port = gridcoin_conf.get('rpcport')
    assert rpc_user
    assert rpc_port
    assert rpc_password
@pytest.fixture
def test_GridcoinClientConnection(test_get_gridcoin_config_parameters):
    global connection_object
    connection_object=main.GridcoinClientConnection(rpc_user=rpc_user, rpc_port=rpc_port, rpc_password=rpc_password)
    assert connection_object
def test_GridcoinClientConnection_run_command(test_GridcoinClientConnection):
    assert connection_object.run_command('listprojects')
    not_found_result=connection_object.run_command('commandthatdoesnotexist')
    assert isinstance(not_found_result,dict)
    assert 'error' in not_found_result
def test_GridcoinClientConnection_get_approved_project_urls(test_GridcoinClientConnection):
    assert connection_object.run_command('listprojects')
    approved_urls_result=connection_object.get_approved_project_urls()
    assert isinstance(approved_urls_result,list)
    assert len(approved_urls_result)>0