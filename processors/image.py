from celery import Celery
import io
from PIL import Image
from time import sleep
import os

celery = Celery('tasks', broker=os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/'), backend='db+sqlite:///backend.sqlite3')
celery.conf.update(
    CELERY_TASK_SERIALIZER = 'pickle',
    CELERY_ACCEPT_CONTENT = ['pickle']
)

@celery.task()
def process_image(image):
    image_bytesio = io.BytesIO(image)
    open_image = Image.open(image_bytesio).convert("RGBA")

    # do some magic
    open_image = open_image.resize((50, 50))
    # and other time consuming stuff
    sleep(5)
    # ...

    return open_image
