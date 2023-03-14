import sys
sys.path.append('./arial-car-track')
from detect_and_track_ooad import Detection
from time import sleep
from django.core.mail import send_mail
from celery import shared_task

@shared_task()
def call_detect(url):
    call_detect = Detection()
    call_detect.detect(url)
    return "Detect Finish"
