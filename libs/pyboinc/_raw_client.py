"""
Raw client for maintaining the socket connection to the BOINC server
Based on:
https://boinc.berkeley.edu/trac/wiki/GuiRpc
https://boinc.berkeley.edu/trac/wiki/GuiRpcProtocol
https://github.com/BOINC/boinc/blob/master/lib/gui_rpc_client.cpp

Note that this client is Async, based on asyncio
"""

import asyncio
from socket import AF_INET
import xml.etree.ElementTree as ET
import sys

GUI_RPC_DEFAULT_PORT = 31416
REPLY_TAG = "boinc_gui_rpc_reply"
REQUEST_TAG = "boinc_gui_rpc_request"
END_OF_MESSAGE = b"\x03"
BOINC_ENCODING = "ISO-8859-1"
PYTHON_VER=sys.version_info

class _RPCClientRaw:
    """
    Connects to the RPC server and transports whichever request and reply to and from it
    Takes and returns XML Element objects
    """

    def __init__(self, host: str, port=GUI_RPC_DEFAULT_PORT):
        self.host = host
        self.port = port
        self._reader = self._writer = None

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port, family=AF_INET, limit=1024*5000)

    async def _write(self, message: bytes):
        if self._writer is None:
            raise ConnectionError("Connection to {} was not opened before writing".format(self.host))
        await self._writer.drain()
        self._writer.write(message + END_OF_MESSAGE)

    async def send(self, request: ET.Element):
        """
        Send request to RPC server
        Returns without guarantee of having finished sending
        """
        req = ET.Element(REQUEST_TAG)
        req.append(request)
        if PYTHON_VER.major>=3 and PYTHON_VER.minor<8:
            req_str = ET.tostring(req, encoding=BOINC_ENCODING, short_empty_elements=True)
        else:
            req_str = ET.tostring(req, encoding=BOINC_ENCODING, xml_declaration=False, short_empty_elements=True)
        req_str = req_str.replace(b" />", b"/>")
        await self._write(req_str)

    async def _read(self):
        if self._reader is None:
            raise ConnectionError("Connection to {} was not opened before writing".format(self.host))
        return await self._reader.readuntil(separator=END_OF_MESSAGE)

    async def receive(self) -> ET.Element:
        """
        Receive the next message by the RPC server
        """
        buff = [await self._read()]
        while buff[-1][-1] != END_OF_MESSAGE[0]:
            buff.append(await self._read())
        resp = "".join(str(b, encoding=BOINC_ENCODING) for b in buff)
        # remove end of message chraracter
        resp = resp[:-1]
        # and parse xml
        resp_e = ET.fromstring(resp)
        try:
            assert resp_e.tag == REPLY_TAG
        except AssertionError:
            raise ConnectionError("Got invalid response from {}".format(self.host))
        return resp_e[0]

    async def request(self, request: ET.Element):
        """
        Send request to server and return reply
        """
        await self.send(request)
        return await self.receive()

