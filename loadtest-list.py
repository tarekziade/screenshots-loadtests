# This is needed for doing the "from utils import (...)" below.
import sys; sys.path.append('.')

import random
import time
import utils

from molotov import (
    global_setup,
    global_teardown,
    scenario,
    setup,
)

NUM_SAMPLE_SHOTS = random.randint(4, 4)


@global_setup()
def login(args):
    async def _create_shot(_):
        return await utils.create_shot()

    async def _create_shot_w_keywords(_):
        return await utils.create_shot(keywords="HIT")

    _login = utils.login(args)

    # Upload X sample shots.
    for x in range(NUM_SAMPLE_SHOTS):
        if (x >= 2):
            res = utils.run_in_fresh_loop(_create_shot_w_keywords)
            assert res.status < 400
        else:
            res = utils.run_in_fresh_loop(_create_shot)
            assert res.status < 400

    time.sleep(5)  # delays for 5 seconds

    return _login


@setup()
async def setup_worker(worker_id, args):
    return utils.setup_worker(worker_id, args)


@global_teardown()
def logout():
    return utils.logout()


@scenario(0)
async def list_shots(session):
    res = await utils.list_shots(session)

    assert res.status == 200

    for shot in res.bod["shots"]:
        clips = shot["json"]["clips"]
        for attr in clips:
            print(clips[attr]["image"]["text"])


@scenario(100)
async def search_shots(session):
    res = await utils.search_shots(session, "HIT")

    assert res.status == 200

    print(res.bod)

    for shot in res.bod["shots"]:
        clips = shot["json"]["clips"]
        for attr in clips:
            print(clips[attr]["image"]["text"])
