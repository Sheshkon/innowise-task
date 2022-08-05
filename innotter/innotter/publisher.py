import pika

from innotter.settings import RABBITMQ_HOSTNAME, RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS

credentials = pika.PlainCredentials(
    username=RABBITMQ_DEFAULT_USER,
    password=RABBITMQ_DEFAULT_PASS
)
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOSTNAME, credentials=credentials, port=5672))
channel = connection.channel()


def publish(body=None):
    channel.basic_publish(exchange='', routing_key='stats', body=body)
