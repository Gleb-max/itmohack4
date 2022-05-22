import base64
import io
import logging
import uuid
from io import StringIO
import cv2
import numpy as np
from PIL import Image
from aiohttp import web
import socketio

from emotion import analyze_image

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

calls = {}


async def index(request):
    with open('templates/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
def connect(sid, environ):
    # print(environ)
    print("connect ", sid)


@sio.event
async def chat_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
async def image(sid, data):
    call_id = data.get('callId')
    data_image = data.get('data')

    # start = time.time()

    sbuf = StringIO()
    sbuf.write(data_image)

    headers, image = data_image.split(',', 1)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    # frame = imutils.resize(frame, width=700)
    # frame = cv2.flip(frame, 1)
    # imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    # stringData = base64.b64encode(imgencode).decode('utf-8')
    # b64_src = 'data:image/jpg;base64,'
    # stringData = b64_src + stringData
    # print("--- %s seconds ---" % (time.time() - start))

    print(calls)
    print(f'image from {sid}')
    for user in calls.get(call_id, []):
        if user != sid:
            # await sio.emit('image_back', stringData, to=user)
            await sio.emit('emotion', analyze_image(frame), to=user)
        else:
            await sio.emit('image_ok', to=sid)


@sio.event
async def createCall(sid):
    call_id = str(uuid.uuid4())
    calls[call_id] = [sid]
    print('createCall')
    print(calls)
    await sio.emit('create_call_success', call_id)


@sio.event
async def joinCall(sid, data):
    call_id = data.get('callId')
    print('joinCall', call_id)
    calls[call_id].append(sid)
    await sio.emit('join_call_success', call_id)


app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=5000)
