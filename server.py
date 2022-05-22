import base64
import uuid
import io
import time
from io import StringIO
import logging
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

calls = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YARIK_NE_GEI'
socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@socketio.on('image')
# @cross_origin()
def image(data):
    call_id = data.get('callId')
    data_image = data.get('data')

    user_id = request.sid
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
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData
    # print("--- %s seconds ---" % (time.time() - start))

    # emit the frame back
    print(calls)
    print(f'image from {user_id}')
    for user in calls.get(call_id, []):
        if user != user_id:
            emit('image_back', stringData, broadcast=True, room=user)
        # else:
        #     emit('image_ok', room=user_id)


@socketio.on('createCall')
# @cross_origin()
def create_call():
    call_id = str(uuid.uuid4())
    calls[call_id] = [request.sid]
    print('createCall')
    print(calls)
    emit('create_call_success', call_id)


@socketio.on('joinCall')
# @cross_origin()
def join_call(data):
    call_id = data.get('callId')
    print('joinCall')
    calls[call_id].append(request.sid)
    emit('join_call_success', call_id)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
