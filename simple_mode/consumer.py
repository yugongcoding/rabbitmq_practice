#!/usr/bin/env python
import pika, sys, os


def main():
    user_info = pika.PlainCredentials('guest', 'guest')  # 用户名和密码
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('192.168.244.240', 5672, '/', user_info))  # 连接服务器上的RabbitMQ服务
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # 只消费一次，关闭连接，关闭channel
    # channel.close()
    # connection.close()
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
