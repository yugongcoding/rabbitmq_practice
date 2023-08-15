#!/usr/bin/env python
import pika
import time

user_info = pika.PlainCredentials('guest', 'guest')  # 用户名和密码
connection = pika.BlockingConnection(
        pika.ConnectionParameters('192.168.244.240', 5672, '/', user_info))  # 连接服务器上的RabbitMQ服务
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(1)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()