#!/usr/bin/env python
import pika
import sys
user_info = pika.PlainCredentials('guest', 'guest')  # 用户名和密码
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.244.240', 5672, '/', user_info))  # 连接服务器上的RabbitMQ服务
channel = connection.channel()

channel.exchange_declare(exchange='pub_sub_logs', exchange_type='fanout')  # 广播交换机

channel.queue_declare(queue='pub_sub_1', durable=True)
channel.queue_declare(queue='pub_sub_2', durable=True)
channel.queue_declare(queue='pub_sub_3', durable=True)

channel.queue_bind(exchange='pub_sub_logs', queue='pub_sub_1')
channel.queue_bind(exchange='pub_sub_logs', queue='pub_sub_2')
channel.queue_bind(exchange='pub_sub_logs', queue='pub_sub_3')


for i in range(100):

    message = ' '.join(sys.argv[1:]) or "info: Hello World! PUB SUB"
    channel.basic_publish(exchange='pub_sub_logs', routing_key='', body=message.encode())
    print(f" [x] Sent {message}")
connection.close()


