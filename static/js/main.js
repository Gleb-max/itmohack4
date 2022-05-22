// var socket = io('http://127.0.0.1:5000/');
// var socket = io('https://ccc7-185-183-34-155.ngrok.io:5000/');
var socket = io({
    'reconnection': false,
    'reconnectionDelay': 1000000,
    'reconnectionDelayMax' : 1000000,
    'reconnectionAttempts': 100,
});

socket.on('connect', function () {
    console.log("Connected...!", socket.connected);
});

const webcamButton = document.getElementById('webcamButton');
const webcamVideo = document.getElementById('webcamVideo');
const callButton = document.getElementById('callButton');
const callInput = document.getElementById('callInput');
const answerButton = document.getElementById('answerButton');
const remoteVideo = document.getElementById('remoteVideo');
const hangupButton = document.getElementById('hangupButton');

// const video = document.querySelector("#videoElement");
webcamVideo.style.display = "none"
// const canvas = document.querySelector("#canvasOutput");

webcamVideo.width = 500;
webcamVideo.height = 375;

webcamButton.onclick = function () {
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: true, audio: true})
            .then(function (stream) {
                webcamVideo.srcObject = stream;
                webcamVideo.play();
            })
            .catch(function (err0r) {
                console.log(err0r);
                console.log("Something went wrong!");
                alert('Не предоставлены разрешения для видео');
            });
    } else {
        alert('Не предоставлены разрешения для видео');
    }

    callButton.disabled = false;
    answerButton.disabled = false;
    webcamButton.disabled = true;
}

callButton.onclick = function () {
    socket.emit('createCall');
}

answerButton.onclick = function () {
    const callId = callInput.value
    if (callId === '') alert('Введите ключ комнаты')
    else {
        socket.emit('joinCall', {'callId': callId});
    }
}

socket.on('create_call_success', function (call_id) {
    console.log('call_id', call_id)
    if (call_id !== undefined) callInput.value = call_id
});

socket.on('join_call_success', function (call_id) {
    if (call_id !== undefined) alert('Вы подключились к комнате')
});


function capture(video, scaleFactor) {
    if (scaleFactor == null) {
        scaleFactor = 1;
    }
    var w = video.videoWidth * scaleFactor;
    var h = video.videoHeight * scaleFactor;
    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, w, h);
    return canvas;
}

function openCvReady() {
    cv['onRuntimeInitialized'] = () => {
        // let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
        // let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
        // let cap = new cv.VideoCapture(video);

        const FPS = 22;

        setInterval(() => {
            // cap.read(src);

            var type = "image/jpg"
            // var data = document.getElementById("canvasOutput").toDataURL(type);
            var frame = capture(webcamVideo, 1)
            var data = frame.toDataURL(type);
            // data = data.replace('data:' + type + ';base64,', ''); //split off junk
            // at the beginning

            const callId = callInput.value
            console.log(callId)
            if (callId !== '') {
                socket.emit(`image`, {'callId': callId, 'data': data});
            }
        }, 10000 / FPS);
    };
}

openCvReady();

socket.on('image_back', function (image) {
    const image_id = document.getElementById('image');
    image_id.src = image;
});
socket.on('image_ok', function (image) {
});
socket.on('emotion', function (emotion) {
    document.getElementById('emotion').innerHTML = emotion;
});
