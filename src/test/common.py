import pytest, os, threading
from aiohttp import web
from ipaddress import IPv4Address
from valve.testing import TestRCONServer

from src.loop import setup_aio
from src.db import models as db
from src.db import Cache
from src.config import ConfigStore, LogLevel, Config

if db.engine == None:
    # special filename "" means in-memory database
    db.init_engine("")

# Force to use a specific config for tests
# Listening to 127.0.0.1 is important because otherwise Github CI gets stuck forever
ConfigStore.cfg = Config(log_level=LogLevel.DEBUG, listen_addr=IPv4Address('127.0.0.1'), log_port_range=(30000,30100))

@pytest.fixture
def client(loop, aiohttp_client):
    app = setup_aio()
    return loop.run_until_complete(aiohttp_client(app))

@pytest.yield_fixture
def rcon_server():
    server = TestRCONServer(address=('127.0.0.1', 0))
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    yield server
    server.shutdown()
    thread.join()
