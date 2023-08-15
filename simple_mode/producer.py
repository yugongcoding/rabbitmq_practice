#!/usr/bin/env python
import pika

user_info = pika.PlainCredentials('guest', 'guest')  # 用户名和密码
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.244.240', 5672, '/', user_info))  # 连接服务器上的RabbitMQ服务


channel = connection.channel()  # 创建channel
channel.queue_declare(queue='hello', durable=True)  # 声明队列，不存在则创建
"""
发消息到hello队列，使用无名交换机发送，指定routing_key和队列名一样，
无名交换机通过routing_key发送到队列，简单模式下不用把队列和交换机以及routing_key绑定
"""
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!'.encode())
print(" [x] Sent 'Hello World!'")
connection.close()



