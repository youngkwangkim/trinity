from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

import serial
import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600)


def is_used(request):
    ser.flushInput()
    serialNumber = ser.readline()

    while 1:
        if (serialNumber == b''):
            ser.flushInput()
            serialNumber = ser.readline()
        else:
            break

    splitSerial = str(serialNumber, 'utf-8').split(' ')

    pir = int(splitSerial[0])
    water = int(splitSerial[1])
    light = int(splitSerial[2])

    onPir = False;
    onWater = False;
    onLight = False;
    isUsedStatus = False;

    if (pir == 1):
        onPir = True
        isUsedStatus = True
    if (water < 300):
        onWater = True
    if (light < 270):
        onLight = True
    
    responseJson = {
        'status': isUsedStatus,
        'data': {
            'water': onWater,
            'light': onLight
        }
    }
    
    return HttpResponse(JSONRenderer().render(responseJson))

