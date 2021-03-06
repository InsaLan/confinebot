from aiohttp import web
import json, pytest, valve.rcon

from .common import client, rcon_server
from src.db import models as db

async def test_match_create(client):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()

    db.session.add(db.Server.Server(ip="10.10.10.1", port=8080, nickname="perdu"))
    db.session.add(db.Team.Team(name="Algebre", nationality="France"))
    db.session.add(db.Team.Team(name="Analyse", nationality="France"))
    db.session.commit()

    data = {
        "idTeamFirstSideT": 1,
        "idTeamFirstSideCT": 2,
        "idServer": 1,
        "map": "de_dust",
        "maxRound": 32,
        "password": "p!k@chu"
    }

    resp = await client.post('/match', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()

    expected = {
      "playAllRound": True,
      "map": "de_dust",
      "streamerReady": False,
      "knifeRound": True,
      "server": {
        "nickname": "perdu",
        "ip": "10.10.10.1",
        "id": 1,
        "port": 8080
      },
      "id": 1,
      "maxRound": 32,
      "teamFirstSideT": {
        "nationality": "France",
        "name": "Algebre",
        "id": 1
      },
      "overtime": True,
      "teamFirstSideCT": {
        "nationality": "France",
        "name": "Analyse",
        "id": 2
      },
      "autostartMatch": True,
      "state": "NOT_STARTED",
      "password": "p!k@chu"
    }

    assert received_data == expected

async def test_match_list(client):
    expected = {
      "playAllRound": True,
      "password": "p!k@chu",
      "map": "de_dust",
      "streamerReady": False,
      "knifeRound": True,
      "server": {
        "nickname": "perdu",
        "ip": "10.10.10.1",
        "id": 1,
        "port": 8080
      },
      "id": 1,
      "maxRound": 32,
      "teamFirstSideT": {
        "nationality": "France",
        "name": "Algebre",
        "id": 1
      },
      "overtime": True,
      "teamFirstSideCT": {
        "nationality": "France",
        "name": "Analyse",
        "id": 2
      },
      "autostartMatch": True,
      "state": "NOT_STARTED"
    }

    resp = await client.get('/match')
    assert resp.status == 200
    received_data = await resp.json()
    assert received_data == [expected]

async def test_match_patch_match_params(client):
    # ensure table is empty before creating Object

    data = {
        "maxRound": 64,
        "overtime": False,
        "autostartMatch": False,
        "knifeRound": False,
        "streamerReady": True
    }
    resp = await client.patch('/match/1', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()
    
    expected_data = {
      "state": "NOT_STARTED",
      "playAllRound": True,
      "password": "p!k@chu",
      "map": "de_dust",
      "streamerReady": True,
      "knifeRound": False,
      "server": {
        "nickname": "perdu",
        "ip": "10.10.10.1",
        "id": 1,
        "port": 8080
      },
      "id": 1,
      "maxRound": 64,
      "teamFirstSideT": {
        "nationality": "France",
        "name": "Algebre",
        "id": 1
      },
      "overtime": False,
      "teamFirstSideCT": {
        "nationality": "France",
        "name": "Analyse",
        "id": 2
      },
      "autostartMatch": False
    }

    assert expected_data == received_data

    # ensure data has been changed accordingly in database
    db_obj = db.session.query(db.Match.Match).one()
    assert db_obj.id == 1
    assert db_obj.maxRound == 64
    assert db_obj.overtime == False
    assert db_obj.autostartMatch == False
    assert db_obj.knifeRound == False
    assert db_obj.streamerReady == True

async def test_match_delete(client):
    resp = await client.delete('/match/1')
    assert resp.status == 204
    
    assert db.session.query(db.Match.Match).count() == 0


async def assert_rcon_messages(rcon_server, msg_list):
    ctr = 1

    for msg in msg_list:
      rcon_server.expect(ctr, valve.rcon.RCONMessage.Type.AUTH_RESPONSE, msg.encode('utf-8'))
      end_of_msg = rcon_server.expect(ctr, valve.rcon.RCONMessage.Type.RESPONSE_VALUE, b"")
      end_of_msg.respond(ctr, valve.rcon.RCONMessage.Type.RESPONSE_VALUE, b"")
      end_of_msg.respond_terminate_multi_part(ctr)
      ctr += 1

async def test_match_setup(client, rcon_server):
    # ensure table is empty before creating Object
    db.session.query(db.Server.Server).delete()
    db.session.query(db.Team.Team).delete()

    p = rcon_server.server_address[1]
    print(rcon_server.server_address) 
     
    db.session.add(db.Server.Server(ip="127.0.0.1", port=p, nickname="perdu"))
    db.session.add(db.Team.Team(name="Algebre", nationality="France"))
    db.session.add(db.Team.Team(name="Analyse", nationality="France"))
    db.session.commit()

    data = {
        "idTeamFirstSideT": 1,
        "idTeamFirstSideCT": 2,
        "idServer": 1,
        "map": "de_dust",
        "maxRound": 32,
        "password": "p!k@chu"
    }

    resp = await client.post('/match', data=json.dumps(data))
    assert resp.status == 200
    received_data = await resp.json()

    expected = {
      "playAllRound": True,
      "map": "de_dust",
      "streamerReady": False,
      "knifeRound": True,
      "server": {
        "nickname": "perdu",
        "ip": "127.0.0.1",
        "id": 1,
        "port": p
      },
      "id": 1,
      "maxRound": 32,
      "teamFirstSideT": {
        "nationality": "France",
        "name": "Algebre",
        "id": 1
      },
      "overtime": True,
      "teamFirstSideCT": {
        "nationality": "France",
        "name": "Analyse",
        "id": 2
      },
      "autostartMatch": True,
      "state": "NOT_STARTED",
     "password": "p!k@chu"
    }

    assert received_data == expected

    auth_request = rcon_server.expect(0, valve.rcon.RCONMessage.Type.AUTH, b"p!k@chu")
    auth_request.respond(0, valve.rcon.RCONMessage.Type.AUTH_RESPONSE, b"")

    await assert_rcon_messages(rcon_server, [
      "log on; mp_logdetail 3;",
      "logaddress_del 127.0.0.1:30000; logaddress_add 127.0.0.1:30000",
      "mp_overtime_maxrounds 32",
      "mp_overtime_enable 1",
      "mp_teamname_1 \"Algebre\"",
      "mp_teamname_2 \"Analyse\"",
    ])

    resp = await client.patch('/match/1', data=json.dumps({'state': 'STARTING'}))
    assert resp.status == 200

    resp = await client.patch('/match/1', data=json.dumps({'state': 'ENDED'}))
    assert resp.status == 200
