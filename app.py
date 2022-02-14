import base64
import io
import logging
import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from processors.image import process_image

app = Flask(__name__)
app.secret_key = 'ABC'
socketio = SocketIO(app)

def encode_image(image):
    image = image.convert('RGB')
    image_bytesoi = io.BytesIO()
    image.save(image_bytesoi, "JPEG")
    return base64.b64encode(image_bytesoi.getvalue()).decode('utf-8')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.files:
            # Save request.files['image, otherwise it will be automaticly closed
            image = request.files['image'].read()

            unique_id = process_image.delay(image).id

            return render_template('processing.html', unique_id=unique_id)
    return render_template('upload.html')

@socketio.on('check_process')
def handle_my_custom_event(unique_id):
    if process_image.AsyncResult(unique_id).status == 'SUCCESS':
        encoded_img_data = encode_image(process_image.AsyncResult(unique_id).get())
        process_image.AsyncResult(unique_id).forget()
        emit('process_finished', encoded_img_data)
    else:
        logging.warn(f'Process status: {process_image.AsyncResult(unique_id).status}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
