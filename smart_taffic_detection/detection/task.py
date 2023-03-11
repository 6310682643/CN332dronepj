from time import sleep
from django.core.mail import send_mail
from celery import shared_task
import sys
sys.path.append('./arial-car-track')
from detect_and_track_ooad import Detection


@shared_task()

def call_detect():
    call_detect = Detection()
    call_detect.detect()
    return "Detect Finish"
