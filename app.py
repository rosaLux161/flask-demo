import os
import time
import json
import io
import base64

from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_executor import Executor
from flask_socketio import SocketIO, emit

from PIL import Image

app = Flask(__name__)
app.secret_key = 'ABC'
app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True
socketio = SocketIO(app)


def save(image):
    image = image.convert('RGB')
    image_bytesoi = io.BytesIO()
    image.save(image_bytesoi, "JPEG")
    return base64.b64encode(image_bytesoi.getvalue()).decode('utf-8')


def process_image(image):
    image_bytesio = io.BytesIO(image)
    open_image = Image.open(image_bytesio).convert("RGBA")

    # do some magic
    open_image = open_image.resize((50, 50))
    # and other time consuming stuff
    time.sleep(5)
    # ...

    return open_image


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            unique_id = request.form['unique_id']

            # Save request.files['image, otherwise it will be automaticly closed
            image = request.files['image'].read()

            executor.submit_stored('exc-'+str(unique_id), process_image, image)
            return render_template('processing.html', unique_id=unique_id)
    return render_template('upload.html')


@socketio.on('process_image')
def handle_my_custom_event(unique_id):
    if not executor.futures.done('exc-'+str(unique_id)):
        future_status = executor.futures._state('exc-'+str(unique_id))
    else:
        future = executor.futures.pop('exc-'+str(unique_id))
        encoded_img_data = save(future.result())
        emit('process_finished', encoded_img_data)


if __name__ == '__main__':
    executor = Executor(app)
    socketio.run(app, host='0.0.0.0', port=int(os.getenv('PORT')))
