# Tests for functions which communicate with BOINC. These will obviously fail if BOINC is not open.
# Note that due to async nature of many BOINC functions, they must be wrapped in loop.run_until_complete()
import datetime

import pytest

import config
import main, asyncio
import libs.pyboinc

rpc_user = None
rpc_port = None
rpc_password = None
CONNECTION_OBJECT: main.BoincClientConnection = None
RPC_CONNECTION_OBJECT: libs.pyboinc.rpc_client.RPCClient = None
loop = asyncio.get_event_loop()
BOINC_DATA_DIR = main.BOINC_DATA_DIR


# Setup BOINC connections
@pytest.fixture
def test_BoincClientConnection():
    global CONNECTION_OBJECT
    CONNECTION_OBJECT = main.BoincClientConnection(config_dir=BOINC_DATA_DIR)
    assert CONNECTION_OBJECT


@pytest.fixture()
def test_setup_connection():
    global RPC_CONNECTION_OBJECT
    RPC_CONNECTION_OBJECT = loop.run_until_complete(
        main.setup_connection(config.BOINC_IP, config.BOINC_PASSWORD, config.BOINC_PORT)
    )
    assert isinstance(RPC_CONNECTION_OBJECT, libs.pyboinc.rpc_client.RPCClient)


def test_BoincClientConnection_get_project_list(test_BoincClientConnection):
    project_list = CONNECTION_OBJECT.get_project_list()
    assert isinstance(project_list, list)
    assert len(project_list) > 3


def test_get_all_projects(test_setup_connection):
    result = loop.run_until_complete(main.get_all_projects(RPC_CONNECTION_OBJECT))
    assert "https://einstein.phys.uwm.edu/" in result
    assert len(result) > 10


def test_get_attached_projects(test_setup_connection):
    result1, result2 = loop.run_until_complete(
        main.get_attached_projects(RPC_CONNECTION_OBJECT)
    )
    assert isinstance(result1, list)
    assert isinstance(result2, dict)
    assert len(result1) > 0
    assert len(result2) > 0
    for project_url in result1:
        assert project_url in result2
    # This will fail if given project is not attached
    assert "https://einstein.phys.uwm.edu/" in result2


def test_verify_boinc_connection(test_setup_connection):
    result1 = loop.run_until_complete(
        main.verify_boinc_connection(RPC_CONNECTION_OBJECT)
    )
    assert result1


def test_prefs_check(test_setup_connection):
    # all requiremente met
    disk_usage = {
        "d_allowed": 100 * 1024 * 1024 * 1024,
    }
    global_prefs = {
        "disk_max_used_gb": 100,
        "net_start_hour": 0,
        "net_end_hour": 0,
    }
    result1 = loop.run_until_complete(
        main.prefs_check(RPC_CONNECTION_OBJECT, global_prefs, disk_usage, True)
    )
    assert result1
    # Disk usage allowed too low
    disk_usage = {
        "d_allowed": 1 * 1024 * 1024 * 1024,
    }
    global_prefs = {
        "disk_max_used_gb": 10,
        "net_start_hour": 0,
        "net_end_hour": 0,
    }
    result1 = loop.run_until_complete(
        main.prefs_check(RPC_CONNECTION_OBJECT, global_prefs, disk_usage, True)
    )
    assert not result1
    disk_usage = {
        "d_allowed": 100 * 1024 * 1024 * 1024,
    }
    global_prefs = {
        "disk_max_used_gb": 8,
        "net_start_hour": 0,
        "net_end_hour": 0,
    }
    result1 = loop.run_until_complete(
        main.prefs_check(RPC_CONNECTION_OBJECT, global_prefs, disk_usage, True)
    )
    assert not result1
    # Not allowed constant network access
    disk_usage = {
        "d_allowed": 100 * 1024 * 1024 * 1024,
    }
    global_prefs = {
        "disk_max_used_gb": 10,
        "net_start_hour": 2,
        "net_end_hour": 0,
    }
    result1 = loop.run_until_complete(
        main.prefs_check(RPC_CONNECTION_OBJECT, global_prefs, disk_usage, True)
    )
    assert not result1
