import json
import os
import random
import time
import uuid
from urllib.parse import urljoin
from molotov import scenario, global_setup, global_teardown

# Read configuration from env
SERVER_URL = os.getenv(
    'URL_PAGESHOT',
    "https://pageshot.stage.mozaws.net").rstrip('/')

example_images = {}
filename = './exercise_images.py'

with open(filename) as f:
    exec(f.read(), example_images)
    example_images = example_images["example_images"]


def make_uuid():
    return str(uuid.uuid1()).replace("-", "")


def make_device_info():
    return dict(
        addonVersion='0.1.2014test',
        platform='test',
    )

deviceInfo = make_device_info()
deviceId = make_uuid()
secret = make_uuid()


def make_example_shot():
    image = random.choice(example_images)
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

text_strings = """
Example strings like apple orange banana some stuff like whatever and whoever and bucket blanket funky etc keyboard screen house window tree leaf leaves feather feathers
""".split()


@global_setup()
def login(args):
    print("Kenny Loggins")

    # TODO: What do we use for "session" here?
    resp = session.post(
        urljoin(SERVER_URL, "/api/login"),
        data=dict(deviceId=deviceId, secret=secret, deviceInfo=json.dumps(deviceInfo))
    )

    if resp.status_code == 404:
        resp = session.post(
            urljoin(SERVER_URL, "/api/register"),
            data=dict(deviceId=deviceId, secret=secret, deviceInfo=json.dumps(deviceInfo))
        )

    resp.raise_for_status()


@global_teardown()
def logout():
    print("logout/delete_account")
    # delete_account()


@scenario(100)
async def create_shot(session):
    path_pageshot = urljoin(SERVER_URL, "data/" + make_uuid() + "/test.com")
    data = make_example_shot()

    try:
        async with session.put(path_pageshot, data=data) as r:
            body = await r.text()
            print("....." + body + "........")

    except Exception as e:
        print(e)
