import pytest, os
from aiohttp import web

from src.loop import setup_aio
from src.db import models as db
from src.db import Cache

if db.engine == None:
    # special filename "" means in-memory database
    db.init_engine("")

@pytest.fixture
def client(loop, aiohttp_client):
    app = setup_aio()
    return loop.run_until_complete(aiohttp_client(app))
