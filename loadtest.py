import os
import uuid
import time
import random
from urllib.parse import urljoin
from molotov import scenario

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

deviceId = make_uuid()

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
        createdDate=int(time.time()*1000),
        favicon=None,
        siteName="test site",
        isPublic=True,
        showPage=False,
        clips={
            make_uuid(): dict(
                createdDate=int(time.time()*1000),
                sortOrder=100,
                image=dict(
                    url=image["url"],
                    captureType="selection",
                    text=text,
                    location=dict(
                        top=100,
                        left=100,
                        bottom=100+image["height"],
                        right=100+image["width"],
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

@scenario(100)
async def create_shot(session):

    #async with session.put(SERVER_URL + STATUS_URL) as r:
    #    body = await r.json()
    #    assert 'user' in body

    shot_id = make_uuid() + "/test.com"
    shot_url = urljoin(SERVER_URL, shot_id)
    shot_data = urljoin(SERVER_URL, "data/" + shot_id)
    resp = make_example_shot()
    async with session.put(shot_data, data=resp) as r:
        body = await r.json()
        print(body)
    #resp.raise_for_status()

