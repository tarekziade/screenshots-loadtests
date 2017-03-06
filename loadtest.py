import json
import os
import random
import time
import uuid
from urllib.parse import urljoin

from molotov import scenario, global_setup, global_teardown, setup
from aiohttp import ClientSession
import asyncio


# Read configuration from env
SERVER_URL = os.getenv(
    'URL_PAGESHOT',
    "https://pageshot.stage.mozaws.net").rstrip('/')


def get_example_images():
    example_images = {}
    with open('./exercise_images.py') as f:
        exec(f.read(), example_images)
        example_images = example_images["example_images"]
    return example_images


def make_uuid():
    return str(uuid.uuid1()).replace("-", "")


def make_device_info():
    return dict(
        addonVersion='0.1.2014test',
        platform='test')


exampleImages = get_example_images()
deviceInfo = make_device_info()
deviceId = make_uuid()
secret = make_uuid()


def make_example_shot():
    image = random.choice(exampleImages)
    text = []
    for i in range(10):
        text.append(random.choice(text_strings))
    text = " ".join(text)
    return dict(
        deviceId=deviceId,
        url="http://test.com/?" + make_uuid(),
        docTitle="Load test page",
        createdDate=int(time.time() * 1000),
        favicon=None,
        siteName="test site",
        isPublic=True,
        showPage=False,
        clips={
            make_uuid(): dict(
                createdDate=int(time.time() * 1000),
                sortOrder=100,
                image=dict(
                    url=image["url"],
                    captureType="selection",
                    text=text,
                    location=dict(
                        top=100,
                        left=100,
                        bottom=100 + image["height"],
                        right=100 + image["width"],
                    ),
                    dimensions=dict(
                        x=image["width"],
                        y=image["height"],
                    ),
                ),
            ),
        },
    )


text_strings = """\
Example strings like apple orange banana some stuff like whatever and whoever
 and bucket blanket funky etc keyboard screen house window tree leaf leaves
 feather feathers""".split()


_COOKIES = None


@global_setup()
def login(args):
    global _COOKIES

    async def _login(loop):
        data = {'deviceId': deviceId,
                'secret': secret,
                'deviceInfo': json.dumps(deviceInfo)}

        login_url = urljoin(SERVER_URL, "/api/login")
        register_url = urljoin(SERVER_URL, "/api/register")

        async with ClientSession(loop=loop) as session:
            async with session.post(login_url, data=data) as resp:
                if resp.status == 404:
                    async with session.post(register_url, data=data) as resp:
                        status = resp.status
                else:
                    status = resp.status

        if status > 399:
            raise AssertionError("Could not login or register")
        return resp.cookies

    _COOKIES = run_in_fresh_loop(_login)
    return {'cookies': _COOKIES}


@setup()
async def setup_worker(worker_id, args):
    return {'cookies': _COOKIES}


@global_teardown()
def logout():
    async def _logout(loop):
        delete_url = urljoin(SERVER_URL, "/leave-page-shot/leave")
        async with ClientSession(cookies=_COOKIES, loop=loop) as session:
            async with session.post(delete_url, data={}) as resp:
                assert resp.status < 400

    run_in_fresh_loop(_logout)


@scenario(100)
async def create_shot(session):
    path_pageshot = urljoin(SERVER_URL, "data/" + make_uuid() + "/test.com")
    data = make_example_shot()
    headers = {'content-type': 'application/json'}

    async with session.put(path_pageshot, data=json.dumps(data), headers=headers) as r:
        assert r.status < 400


def run_in_fresh_loop(coro):
    loop = asyncio.new_event_loop()
    task = loop.create_task(coro(loop))
    res = loop.run_until_complete(task)
    loop.close()
    return res
