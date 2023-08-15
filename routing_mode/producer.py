#!/usr/bin/env python
import pika
import sys
user_info = pika.PlainCredentials('guest', 'guest')  # 用户名和密码
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.244.240', 5672, '/', user_info))  # 连接服务器上的RabbitMQ服务
channel = connection.channel()

channel.exchange_declare(exchange='routing_logs', exchange_type='direct')  # 路由交换机

channel.queue_declare(queue='routing_info', durable=True)
channel.queue_declare(queue='routing_error', durable=True)

channel.queue_bind(exchange='routing_logs', queue='routing_info', routing_key='routing_info')
channel.queue_bind(exchange='routing_logs', queue='routing_error', routing_key='routing_error')


for i in range(100):

    message = ' '.join(sys.argv[1:]) or "info: Hello World! ROUTING"
    channel.basic_publish(exchange='routing_logs', routing_key='routing_info', body=message.encode())
    print(f" [x] Sent {message}")
for i in range(50):

    message = ' '.join(sys.argv[1:]) or "info: Hello World! ROUTING"
    channel.basic_publish(exchange='routing_logs', routing_key='routing_error', body=message.encode())
    print(f" [x] Sent {message}")
connection.close()


