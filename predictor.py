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
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='clf_demo')

MODELFILE = 'clf_model.sav'
loaded_model = pickle.load(open(MODELFILE, 'rb'))

def predictFunc(x_test):
    print('called predictFunc')
    y_hat = loaded_model.predict(x_test)
    result = 'Metal'
    if int(y_hat[0]) == 0:
        result = 'Rock'
    print(result)
    return result

def callbackMQ(ch, method, properties, body):
    x_test = np.array(json.loads(body)).reshape((1,60))
    channel.basic_publish(exchange='', 
                          routing_key='clf_demo', 
                          body=predictFunc(x_test)
                         )

channel.basic_consume(
    queue='clf_demo', 
    on_message_callback=callbackMQ, 
    auto_ack=True
    )

def sig_end_handler(sig, frame):
    print('Predictor System shutting down...')
    channel.stop_consuming()
    channel.close()
    sys.exit(0)
signal.signal(signal.SIGINT, sig_end_handler)
print("Predictor consumer starting..")
channel.start_consuming()

