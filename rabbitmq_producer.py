# coding=utf-8
### 生产者

import pika
import time

user_info = pika.PlainCredentials('guest', 'guest')  # 用户名和密码
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.244.240', 5672, '/', user_info))  # 连接服务器上的RabbitMQ服务

# 创建一个channel
channel = connection.channel()
channel.queue_bind()
# 如果指定的queue不存在，则会创建一个queue，如果已经存在 则不会做其他动作，官方推荐，每次使用时都可以加上这句
channel.queue_declare(queue='hello_world')
for i in range(0, 10):
    print(i)
    channel.basic_publish(exchange='',  # 当前是一个简单模式，所以这里设置为空字符串就可以了
                          routing_key='hello_world',  # 指定消息要发送到哪个queue
                          body='{}'.format(i).encode()  # 指定要发送的消息
                          )

# 关闭连接
connection.close()
