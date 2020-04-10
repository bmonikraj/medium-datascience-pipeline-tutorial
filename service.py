#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 01:28:17 2020

@author: bmonikraj
"""

from flask import Flask, request
import pika
from time import sleep
import sys
import uuid
import signal
import threading

RABBITMQ_CONN = 'amqp://qgiopyqq:7oJ-H0oogyJglZ3bP92sdRtIWiu-J6pX@vulture.rmq.cloudamqp.com/qgiopyqq'
params = pika.URLParameters(RABBITMQ_CONN)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='clf_demo')

#internal_lock = threading.Lock()
response_queue = {}


def _on_response(ch, method, props, body):
    """On response we simply store the result in a local dictionary."""
    print('on_response', body)
    response_queue[props.correlation_id] = body

def _process_data_events():
    """Check for incoming data events.
    We do this on a thread to allow the flask instance to send
    asynchronous requests.
    It is important that we lock the thread each time we check for events.
    """
    connectionC = pika.BlockingConnection(params)
    channelC = connectionC.channel()
    channelC.queue_declare(queue='clf_demo')
    channelC.basic_consume(on_message_callback=_on_response, queue='clf_demo')
    print("Service consumer starting...")
    channelC.start_consuming()
            
thread = threading.Thread(target=_process_data_events)
thread.setDaemon(True)
thread.start()

app = Flask(__name__)

def sig_end_handler(sig, frame):
    print('Service System shutting down...')
    sys.exit(0)
signal.signal(signal.SIGINT, sig_end_handler)

@app.route('/predict', methods=['POST'])
def predict():
    x_test = request.form['params']
    corr_id = str(uuid.uuid4())
    response_queue[corr_id] = None
    channel.basic_publish(exchange='',
                           routing_key='clf_demo',
                           properties=pika.BasicProperties(
                               correlation_id=corr_id,
                           ),
                           body=x_test)
    while response_queue[corr_id] is None:
        print(response_queue)
        sleep(0.1)
    resultData = response_queue[corr_id]
    print(resultData)
    del response_queue[corr_id]
    return resultData

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

