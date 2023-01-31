#!/usr/bin/env python
# -*- coding: utf-8 -*-

# general requirements
import unittest

# For the tests
import asyncio
from pyboinc import init_rpc_client
from pyboinc.rpc_client import GUI_RPC_DEFAULT_PORT

ADDRESS = 'localhost'


class BoincTest(unittest.TestCase):

    server = None
    server_control = None
    port = GUI_RPC_DEFAULT_PORT
    url = 'localhost'
    rpc_client = None

    def setUp(self):

        async def init(self):
            self.rpc_client = await init_rpc_client(self.url, None, self.url)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(init(self))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
