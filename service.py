#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 01:28:17 2020

@author: bmonikraj
"""

import pika
from time import sleep
import sys
import uuid
import signal
import asyncio
import websockets
import json

RABBITMQ_CONN = 'amqp://qgiopyqq:7oJ-H0oogyJglZ3bP92sdRtIWiu-J6pX@vulture.rmq.cloudamqp.com/qgiopyqq'
params = pika.URLParameters(RABBITMQ_CONN)

response_queue = {}

def sig_end_handler(sig, frame):
    print('Service System shutting down...')
    sys.exit(0)
signal.signal(signal.SIGINT, sig_end_handler)

def _on_response(ch, method, props, body):
    resBody = json.loads(body)
    global response_queue
    response_queue[resBody['corrId']] = resBody['response']
    ch.close()

async def predict(websocket, path):
    body = await websocket.recv()
    uuidString = str(uuid.uuid4())
    reqBody = {}
    reqBody['corrId'] = uuidString
    reqBody['body'] = json.loads(body)

    connectionReq = pika.BlockingConnection(params)
    channelReq = connectionReq.channel()
    channelReq.queue_declare(queue='clf_demo_req')
    channelReq.basic_publish(exchange='',
                     routing_key='clf_demo_req',
                     body=str(json.dumps(reqBody)))
    channelReq.close()
    connectionRes = pika.BlockingConnection(params)
    channelRes = connectionRes.channel()
    channelRes.queue_declare(queue='clf_demo_res')
    channelRes.basic_consume(on_message_callback=_on_response, queue='clf_demo_res', auto_ack=True)
    print("Service consumer starting...")
    channelRes.start_consuming()
    print("channel closed")
    global response_queue
    result = str(response_queue[uuidString])
    del response_queue[uuidString]
    await websocket.send(result)

start_server = websockets.serve(predict, "0.0.0.0", 8765)
print("starting server ")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
