#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 01:16:23 2020

@author: bmonikraj
"""

import pickle
import json
import pika
import sys
import signal
import numpy as np

RABBITMQ_CONN = 'amqp://qgiopyqq:7oJ-H0oogyJglZ3bP92sdRtIWiu-J6pX@vulture.rmq.cloudamqp.com/qgiopyqq'
params = pika.URLParameters(RABBITMQ_CONN)
connectionReq = pika.BlockingConnection(params)
channelReq = connectionReq.channel()
channelReq.queue_declare(queue='clf_demo_req')
connectionRes = pika.BlockingConnection(params)
channelRes = connectionRes.channel()
channelRes.queue_declare(queue='clf_demo_res')

MODELFILE = 'clf_model.sav'
loaded_model = pickle.load(open(MODELFILE, 'rb'))

def predictFunc(x_test, corrId):
    y_hat = loaded_model.predict(x_test)
    result = 'Metal type'
    if int(y_hat[0]) == 0:
        result = 'Rock type'
    return {
        'corrId' : corrId,
        'response' : result
    }

def callbackMQ(ch, method, properties, body):
    x_test = np.array(json.loads(body)['body']).reshape((1,60))
    corrId = json.loads(body)['corrId']
    sendData = json.dumps(predictFunc(x_test, corrId))
    channelRes.basic_publish(exchange='',
                          routing_key='clf_demo_res',
                          body=str(sendData)
                         )

channelReq.basic_consume(
    queue='clf_demo_req',
    on_message_callback=callbackMQ,
    auto_ack=True
    )

def sig_end_handler(sig, frame):
    print('Predictor System shutting down...')
    channelReq.stop_consuming()
    channelReq.close()
    channelRes.close()
    sys.exit(0)
signal.signal(signal.SIGINT, sig_end_handler)
print("Predictor consumer starting..")
channelReq.start_consuming()
