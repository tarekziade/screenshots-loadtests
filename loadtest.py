# This is needed for doing the "from utils import (...)" below.
import sys; sys.path.append('.')

import json
import os
from urllib.parse import urljoin

import utils

from molotov import (
    scenario,
    global_setup,
    global_teardown,
    setup,
)

WEIGHT_CREATE_SHOT = int(os.getenv('WEIGHT_CREATE_SHOT') or '0')
WEIGHT_READ_SHOT = int(os.getenv('WEIGHT_READ_SHOT') or '0')


@global_setup()
def login(args):
    return utils.login(args)


@setup()
async def setup_worker(worker_id, args):
    return utils.setup_worker(worker_id, args)


@global_teardown()
def logout():
    return utils.logout()


@scenario(WEIGHT_CREATE_SHOT)
async def create_shot(session):
    res = await utils.create_shot(session)
    assert res.status < 400


# @scenario(WEIGHT_READ_SHOT)
# async def read_shot(session):
#     shot = await utils.create_shot(session)
#     assert shot.status < 400

#     res = await utils.read_shot(session, shot.path)
#     assert res.status < 400
