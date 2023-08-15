import pika


class Producer:
    def __init__(self):
        self.user = "guest"
        self.pwd = "guest"
        self.ip = "192.168.244.240"
        self.port = 5672

    def __call__(self):
        self.producer()

    def define_dead_ex_queue(self):
        credentials = pika.PlainCredentials(self.user, self.pwd)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip, self.port, '/', credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange='dead_exchange', exchange_type='direct')
        channel.queue_declare(queue='dead_queue', durable=True)
        channel.queue_bind(queue='dead_queue', routing_key='dead_queue', exchange='dead_exchange')
        connection.close()

    def producer(self):
        credentials = pika.PlainCredentials(self.user, self.pwd)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip, self.port, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(
            passive=True,
            queue="normal_queue",
            arguments={
                'x-max-length': 20,
                'x-dead-letter-exchange': 'dead_exchange',
                'x-dead-letter-routing-key': 'dead_queue',
                'x-message-ttl': 5000
            }, durable=True)
        for i in range(100):
            channel.basic_publish(
                exchange='',
                routing_key='normal_queue',
                body="dead letter".encode(),
                # properties=pika.BasicProperties(expiration="5000"),
            )
        connection.close()  # 连接关闭


def main():
    c = Producer()
    c.define_dead_ex_queue()
    c()
    print('...... over')


if __name__ == '__main__':
    main()