from .views import edit_status
import sys
sys.path.append('./arial-car-track')
from detect_and_track_ooad import Detection
from celery import shared_task
from django.core.mail import send_mail
from time import sleep



@shared_task()
def call_detect(url, id):
    edit_status(1, id)
    call_detect = Detection()
    call_detect.detect(url)
    edit_status(2, id)
    return "Detect Finish"
